import json

import jubilant
from tests.unit.fake_spaces import SPACES_LIST, SPACES_LIST_EMPTY

from . import mocks


def test_list(run: mocks.Run):
    run.handle(
        ['juju', 'spaces', '--format', 'json'],
        stdout=json.dumps(SPACES_LIST),
    )
    juju = jubilant.Juju()

    result = juju.spaces()

    assert len(result) == 2
    assert result[0] == jubilant.Space(
        id='0',
        name='alpha',
        subnets={
            '172.31.0.0/20': jubilant.SpaceSubnet(
                type='ipv4',
                provider_id='subnet-abc123',
                status='in-use',
                zones=('us-east-1a', 'us-east-1b'),
            ),
            '10.0.0.0/24': jubilant.SpaceSubnet(
                type='ipv4',
                status='in-use',
                zones=('us-east-1a',),
            ),
        },
    )
    assert result[1] == jubilant.Space(id='1', name='db-space')


def test_empty(run: mocks.Run):
    run.handle(
        ['juju', 'spaces', '--format', 'json'],
        stdout=json.dumps(SPACES_LIST_EMPTY),
    )
    juju = jubilant.Juju()

    result = juju.spaces()
    assert result == []


def test_with_model(run: mocks.Run):
    run.handle(
        ['juju', 'spaces', '--model', 'mdl', '--format', 'json'],
        stdout=json.dumps(SPACES_LIST_EMPTY),
    )
    juju = jubilant.Juju(model='mdl')

    result = juju.spaces()
    assert result == []
