import json

import jubilant

from . import mocks

SPACES_OUTPUT = {
    'spaces': [
        {
            'id': '0',
            'name': 'alpha',
            'subnets': {
                '10.240.88.0/24': {
                    'type': 'ipv4',
                    'provider-id': 'subnet-lxdbr0-10.240.88.0/24',
                    'status': 'in-use',
                    'zones': ['zone1'],
                }
            },
        }
    ]
}


def test_defaults(run: mocks.Run):
    run.handle(
        ['juju', 'spaces', '--format', 'json'],
        stdout=json.dumps(SPACES_OUTPUT),
    )
    juju = jubilant.Juju()

    result = juju.spaces()

    assert len(result['spaces']) == 1
    assert result['spaces'][0]['name'] == 'alpha'


def test_with_model(run: mocks.Run):
    run.handle(
        ['juju', 'spaces', '--model', 'mdl', '--format', 'json'],
        stdout=json.dumps(SPACES_OUTPUT),
    )
    juju = jubilant.Juju(model='mdl')

    result = juju.spaces()

    assert result['spaces'][0]['name'] == 'alpha'
