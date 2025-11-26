from __future__ import annotations

import pathlib
import subprocess
import tempfile
from typing import Generator

import pytest

import jubilant

pytestmark = pytest.mark.machine


@pytest.fixture(scope='module', autouse=True)
def setup(juju: jubilant.Juju):
    juju.deploy('ubuntu')
    juju.wait(jubilant.all_active)


@pytest.fixture(scope='module')
def private_key_file(juju: jubilant.Juju) -> Generator[str]:
    with tempfile.NamedTemporaryFile(delete=False, dir=juju._temp_dir) as f:
        temp_file = f.name

    public_key = None
    try:
        subprocess.run(
            ['/usr/bin/ssh-keygen', '-t', 'ed25519', '-f', temp_file, '-N', '""', '-q'], check=True
        )
        with open(temp_file + '.pub') as keyfile:
            public_key = keyfile.read()
        juju.add_ssh_key(public_key)
        yield temp_file
    finally:
        if public_key:
            juju.remove_ssh_key(public_key)
        pathlib.Path(temp_file).unlink(missing_ok=True)
        pathlib.Path(temp_file + '.pub').unlink(missing_ok=True)


def test_exec(juju: jubilant.Juju):
    task = juju.exec('echo foo', machine=0)
    assert task.success
    assert task.return_code == 0
    assert task.stdout == 'foo\n'
    assert task.stderr == ''

    task = juju.exec('echo', 'bar', 'baz', machine=0)
    assert task.success
    assert task.stdout == 'bar baz\n'


def test_ssh(juju: jubilant.Juju, private_key_file: str):
    output = juju.ssh('ubuntu/0', 'echo', 'UNIT', ssh_options=['-i', private_key_file])
    assert output == 'UNIT\n'

    output = juju.ssh(0, 'echo', 'MACHINE', ssh_options=['-i', private_key_file])
    assert output == 'MACHINE\n'


def test_add_and_remove_unit(juju: jubilant.Juju):
    juju.add_unit('ubuntu')
    juju.wait(lambda status: jubilant.all_active(status) and len(status.apps['ubuntu'].units) == 2)

    juju.remove_unit('ubuntu/1')
    juju.wait(lambda status: jubilant.all_active(status) and len(status.apps['ubuntu'].units) == 1)
