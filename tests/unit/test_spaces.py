import json

import jubilant

from . import mocks


def test_add_space_no_subnets(run: mocks.Run):
    run.handle(['juju', 'add-space', '--model', 'mdl', 'myspace'])
    juju = jubilant.Juju(model='mdl')

    juju.add_space('myspace')


def test_add_space_one_subnet(run: mocks.Run):
    run.handle(['juju', 'add-space', 'myspace', '192.168.1.0/24'])
    juju = jubilant.Juju()

    juju.add_space('myspace', '192.168.1.0/24')


def test_add_space_multiple_subnets(run: mocks.Run):
    run.handle(['juju', 'add-space', 'myspace', '192.168.1.0/24', '10.0.0.0/8'])
    juju = jubilant.Juju()

    juju.add_space('myspace', '192.168.1.0/24', '10.0.0.0/8')


def test_remove_space(run: mocks.Run):
    run.handle(['juju', 'remove-space', 'myspace'])
    juju = jubilant.Juju()

    juju.remove_space('myspace')


def test_remove_space_force(run: mocks.Run):
    run.handle(['juju', 'remove-space', 'myspace', '--force'])
    juju = jubilant.Juju()

    juju.remove_space('myspace', force=True)


def test_rename_space(run: mocks.Run):
    run.handle(['juju', 'rename-space', 'oldname', 'newname'])
    juju = jubilant.Juju()

    juju.rename_space('oldname', 'newname')


def test_move_to_space_one_subnet(run: mocks.Run):
    run.handle(['juju', 'move-to-space', 'myspace', '192.168.1.0/24'])
    juju = jubilant.Juju()

    juju.move_to_space('myspace', '192.168.1.0/24')


def test_move_to_space_multiple_subnets(run: mocks.Run):
    run.handle(['juju', 'move-to-space', 'myspace', '192.168.1.0/24', '10.0.0.0/8'])
    juju = jubilant.Juju()

    juju.move_to_space('myspace', '192.168.1.0/24', '10.0.0.0/8')


def test_move_to_space_force(run: mocks.Run):
    run.handle(['juju', 'move-to-space', 'myspace', '192.168.1.0/24', '--force'])
    juju = jubilant.Juju()

    juju.move_to_space('myspace', '192.168.1.0/24', force=True)


def test_reload_spaces(run: mocks.Run):
    run.handle(['juju', 'reload-spaces'])
    juju = jubilant.Juju()

    juju.reload_spaces()


def test_reload_spaces_with_model(run: mocks.Run):
    run.handle(['juju', 'reload-spaces', '--model', 'mdl'])
    juju = jubilant.Juju(model='mdl')

    juju.reload_spaces()


def test_show_space(run: mocks.Run):
    output = {
        'myspace': {
            'subnets': ['192.168.1.0/24', '10.0.0.0/8'],
        }
    }
    run.handle(
        ['juju', 'show-space', 'myspace', '--format', 'json'],
        stdout=json.dumps(output),
    )
    juju = jubilant.Juju()

    space = juju.show_space('myspace')

    assert space.name == 'myspace'
    assert len(space.subnets) == 2
    assert space.subnets[0].cidr == '192.168.1.0/24'
    assert space.subnets[1].cidr == '10.0.0.0/8'


def test_show_space_complex_subnets(run: mocks.Run):
    output = {
        'myspace': {
            'subnets': [
                {
                    'cidr': '192.168.1.0/24',
                    'provider-id': 'subnet-123',
                    'provider-space-id': 'space-456',
                    'provider-network-id': 'net-789',
                    'vlan-tag': 100,
                    'zones': ['us-east-1a', 'us-east-1b'],
                }
            ],
        }
    }
    run.handle(
        ['juju', 'show-space', 'myspace', '--format', 'json'],
        stdout=json.dumps(output),
    )
    juju = jubilant.Juju()

    space = juju.show_space('myspace')

    assert space.name == 'myspace'
    assert len(space.subnets) == 1
    assert space.subnets[0].cidr == '192.168.1.0/24'
    assert space.subnets[0].provider_id == 'subnet-123'
    assert space.subnets[0].provider_space_id == 'space-456'
    assert space.subnets[0].provider_network_id == 'net-789'
    assert space.subnets[0].vlan_tag == 100
    assert space.subnets[0].zones == ['us-east-1a', 'us-east-1b']


def test_spaces(run: mocks.Run):
    output = {
        'alpha': {
            'subnets': ['192.168.1.0/24'],
        },
        'beta': {
            'subnets': ['10.0.0.0/8'],
        },
    }
    run.handle(
        ['juju', 'spaces', '--format', 'json'],
        stdout=json.dumps(output),
    )
    juju = jubilant.Juju()

    spaces = juju.spaces()

    assert len(spaces) == 2
    space_names = {space.name for space in spaces}
    assert 'alpha' in space_names
    assert 'beta' in space_names
    # Find the alpha space
    alpha = next(s for s in spaces if s.name == 'alpha')
    assert len(alpha.subnets) == 1
    assert alpha.subnets[0].cidr == '192.168.1.0/24'


def test_spaces_empty(run: mocks.Run):
    output = {}
    run.handle(
        ['juju', 'spaces', '--format', 'json'],
        stdout=json.dumps(output),
    )
    juju = jubilant.Juju()

    spaces = juju.spaces()

    assert len(spaces) == 0
