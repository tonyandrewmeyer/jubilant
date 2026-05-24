import json

import jubilant
from tests.unit.fake_spaces import SHOW_SPACE, SHOW_SPACE_MINIMAL

from . import mocks


def test_full(run: mocks.Run):
    run.handle(
        ['juju', 'show-space', 'alpha', '--format', 'json'],
        stdout=json.dumps(SHOW_SPACE),
    )
    juju = jubilant.Juju()

    info = juju.show_space('alpha')

    assert info == jubilant.ShowSpaceInfo(
        space=jubilant.SpaceInfo(
            id='0',
            name='alpha',
            subnets=(
                jubilant.SubnetInfo(
                    cidr='172.31.0.0/20',
                    vlan_tag=0,
                    provider_id='subnet-abc123',
                    provider_space_id='prov-space-1',
                    provider_network_id='vpc-123',
                    zones=('us-east-1a', 'us-east-1b'),
                ),
                jubilant.SubnetInfo(
                    cidr='10.0.0.0/24',
                    vlan_tag=42,
                    zones=('us-east-1a',),
                ),
            ),
        ),
        applications=('mysql', 'wordpress'),
        machine_count=3,
    )


def test_minimal(run: mocks.Run):
    run.handle(
        ['juju', 'show-space', 'empty-space', '--format', 'json'],
        stdout=json.dumps(SHOW_SPACE_MINIMAL),
    )
    juju = jubilant.Juju()

    info = juju.show_space('empty-space')

    assert info == jubilant.ShowSpaceInfo(
        space=jubilant.SpaceInfo(id='2', name='empty-space'),
    )
    assert info.applications == ()
    assert info.machine_count == 0


def test_with_model(run: mocks.Run):
    run.handle(
        ['juju', 'show-space', '--model', 'mdl', 'alpha', '--format', 'json'],
        stdout=json.dumps(SHOW_SPACE),
    )
    juju = jubilant.Juju(model='mdl')

    info = juju.show_space('alpha')
    assert info.space.name == 'alpha'
