from __future__ import annotations

import json
from typing import Any

import jubilant

from . import mocks

SHOW_SPACE_OUTPUT: dict[str, Any] = {
    'space': {
        'id': '0',
        'name': 'alpha',
        'subnets': [
            {
                'cidr': '10.240.88.0/24',
                'provider-id': 'subnet-lxdbr0-10.240.88.0/24',
                'provider-network-id': 'net-lxdbr0',
                'vlan-tag': 0,
                'zones': ['zone1'],
            }
        ],
    },
    'applications': [],
    'machine-count': 0,
}


def test_defaults(run: mocks.Run):
    run.handle(
        ['juju', 'show-space', '--format', 'json', 'alpha'],
        stdout=json.dumps(SHOW_SPACE_OUTPUT),
    )
    juju = jubilant.Juju()

    result = juju.show_space('alpha')

    assert result['space']['name'] == 'alpha'
    assert result['space']['subnets'][0]['cidr'] == '10.240.88.0/24'
    assert result['machine-count'] == 0


def test_with_model(run: mocks.Run):
    run.handle(
        ['juju', 'show-space', '--model', 'mdl', '--format', 'json', 'alpha'],
        stdout=json.dumps(SHOW_SPACE_OUTPUT),
    )
    juju = jubilant.Juju(model='mdl')

    result = juju.show_space('alpha')

    assert result['space']['name'] == 'alpha'
