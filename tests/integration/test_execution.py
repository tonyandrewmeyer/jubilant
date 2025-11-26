from __future__ import annotations

import pathlib
import subprocess
import tempfile
from typing import Generator

import pytest

import jubilant

from . import helpers


@pytest.fixture(scope='module', autouse=True)
def setup(juju: jubilant.Juju):
    juju.deploy(helpers.find_charm('testdb'))
    juju.wait(
        lambda status: status.apps['testdb'].units['testdb/0'].workload_status.current == 'unknown'
    )


@pytest.fixture(scope='module')
def ssh_key_pair(juju: jubilant.Juju) -> Generator[tuple[str, str]]:
    subprocess.run(['/usr/bin/apt', 'update'], check=True)
    subprocess.run(['/usr/bin/apt', 'install', '-y', 'openssh-client'], check=True)

    with tempfile.NamedTemporaryFile(delete=False, dir=juju._temp_dir) as f:
        temp_file = f.name

    try:
        subprocess.run(
            ['/usr/bin/ssh-keygen', '-t', 'ed25519', '-f', temp_file, '-N', '""', '-q'], check=True
        )
        with open(temp_file + '.pub') as keyfile:
            public_key = keyfile.read()
        yield public_key, temp_file
    finally:
        pathlib.Path(temp_file).unlink(missing_ok=True)
        pathlib.Path(temp_file + '.pub').unlink(missing_ok=True)


def test_run_success(juju: jubilant.Juju):
    juju.config('testdb', {'testoption': 'foobar'})

    task = juju.run('testdb/0', 'do-thing', {'param1': 'value1'})
    assert task.success
    assert task.return_code == 0
    assert task.results == {
        'config': {'testoption': 'foobar'},
        'params': {'param1': 'value1'},
        'thingy': 'foo',
    }


def test_run_leader(juju: jubilant.Juju):
    task = juju.run('testdb/leader', 'do-thing', {'param2': 'value2'})
    assert task.success
    assert task.results == {
        'config': {'testoption': 'foobar'},
        'params': {'param2': 'value2'},
        'thingy': 'foo',
    }


def test_run_error(juju: jubilant.Juju):
    with pytest.raises(jubilant.TaskError) as excinfo:
        juju.run('testdb/0', 'do-thing', {'error': 'ERR'})
    task = excinfo.value.task
    assert not task.success
    assert task.status == 'failed'
    assert task.return_code == 0  # return_code is 0 even if action fails
    assert task.message == 'failed with error: ERR'


def test_run_exception(juju: jubilant.Juju):
    with pytest.raises(jubilant.TaskError) as excinfo:
        juju.run('testdb/0', 'do-thing', {'exception': 'EXC'})
    task = excinfo.value.task
    assert not task.success
    assert task.status == 'failed'
    assert task.return_code != 0
    assert 'EXC' in task.stderr


def test_run_timeout(juju: jubilant.Juju):
    with pytest.raises(TimeoutError):
        juju.run('testdb/0', 'do-thing', wait=0.001)


def test_run_action_not_defined(juju: jubilant.Juju):
    with pytest.raises(ValueError):
        juju.run('testdb/0', 'action-not-defined')


def test_run_unit_not_found(juju: jubilant.Juju):
    with pytest.raises(ValueError):
        juju.run('testdb/42', 'do-thing')


def test_exec_success(juju: jubilant.Juju):
    task = juju.exec('echo foo', unit='testdb/0')
    assert task.success
    assert task.return_code == 0
    assert task.stdout == 'foo\n'
    assert task.stderr == ''

    task = juju.exec('echo', 'bar', 'baz', unit='testdb/0')
    assert task.success
    assert task.stdout == 'bar baz\n'


def test_exec_leader(juju: jubilant.Juju):
    task = juju.exec('echo foo', unit='testdb/leader')
    assert task.success
    assert task.stdout == 'foo\n'


def test_exec_error(juju: jubilant.Juju):
    with pytest.raises(jubilant.TaskError) as excinfo:
        juju.exec('sleep x', unit='testdb/0')
    task = excinfo.value.task
    assert not task.success
    assert task.stdout == ''
    assert 'invalid time' in task.stderr


def test_exec_timeout(juju: jubilant.Juju):
    with pytest.raises(TimeoutError):
        juju.exec('sleep 1', unit='testdb/0', wait=0.001)


def test_exec_unit_not_found(juju: jubilant.Juju):
    with pytest.raises(ValueError):
        juju.exec('echo foo', unit='testdb/42')


def test_exec_error_machine_on_k8s(juju: jubilant.Juju):
    with pytest.raises(jubilant.CLIError):
        juju.exec('echo foo', machine=0)


def test_add_ssh_key(juju: jubilant.Juju, ssh_key_pair: tuple[str, str]):
    juju.add_ssh_key(ssh_key_pair[0])
    # The key will be used in subsequent tests.


def test_ssh(juju: jubilant.Juju, ssh_key_pair: tuple[str, str]):
    # The 'testdb' charm doesn't have any containers, so use 'snappass-test'.
    juju.deploy('snappass-test')
    juju.wait(lambda status: jubilant.all_active(status, 'snappass-test'))

    ssh_options = ['-i', ssh_key_pair[1]]
    output = juju.ssh('snappass-test/0', 'ls', '/charm/containers', ssh_options=ssh_options)
    assert output.split() == ['redis', 'snappass']
    output = juju.ssh(
        'snappass-test/0', 'ls', '/charm/container', container='snappass', ssh_options=ssh_options
    )
    assert 'pebble' in output.split()
    output = juju.ssh(
        'snappass-test/0', 'ls', '/charm/container', container='redis', ssh_options=ssh_options
    )
    assert 'pebble' in output.split()


def test_scp(juju: jubilant.Juju, ssh_key_pair: tuple[str, str]):
    scp_options = ['-i', ssh_key_pair[1]]
    juju.scp(
        'snappass-test/0:agents/unit-snappass-test-0/charm/src/charm.py',
        'charm.py',
        scp_options=scp_options,
    )
    charm_src = pathlib.Path('charm.py').read_text()
    assert 'class Snappass' in charm_src

    juju.scp('snappass-test/0:/etc/passwd', 'passwd', container='redis', scp_options=scp_options)
    passwd = pathlib.Path('passwd').read_text()
    assert 'redis:' in passwd

    # Test a round trip
    with tempfile.NamedTemporaryFile('w+') as fsrc, tempfile.NamedTemporaryFile('w+') as fdst:
        fsrc.write('roundtrip')
        fsrc.flush()
        juju.scp(fsrc.name, 'snappass-test/0:/tmp/roundtrip.py', scp_options=scp_options)
        juju.scp('snappass-test/0:/tmp/roundtrip.py', fdst.name, scp_options=scp_options)
        assert pathlib.Path(fdst.name).read_text() == 'roundtrip'


def test_cli_input(juju: jubilant.Juju, ssh_key_pair: tuple[str, str]):
    stdout = juju.cli(
        'ssh', '--container', 'charm', 'testdb/0', '-i', ssh_key_pair[1], 'cat', stdin='foo'
    )
    assert stdout == 'foo'


def test_remove_ssh_key(juju: jubilant.Juju, ssh_key_pair: tuple[str, str]):
    public_key, private_key_file = ssh_key_pair
    juju.remove_ssh_key(public_key)
    with pytest.raises(jubilant.CLIError, match='Permission denied'):
        juju.ssh(
            'snappass-test/0', 'ls', '/charm/containers', ssh_options=['-i', private_key_file]
        )
