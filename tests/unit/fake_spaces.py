"""Fake data for space-related unit tests."""

from __future__ import annotations

from typing import Any

SPACES_LIST: dict[str, Any] = {
    'spaces': [
        {
            'id': '0',
            'name': 'alpha',
            'subnets': {
                '172.31.0.0/20': {
                    'type': 'ipv4',
                    'provider-id': 'subnet-abc123',
                    'status': 'in-use',
                    'zones': ['us-east-1a', 'us-east-1b'],
                },
                '10.0.0.0/24': {
                    'type': 'ipv4',
                    'status': 'in-use',
                    'zones': ['us-east-1a'],
                },
            },
        },
        {
            'id': '1',
            'name': 'db-space',
            'subnets': {},
        },
    ],
}

SPACES_LIST_EMPTY: dict[str, Any] = {
    'spaces': [],
}

SHOW_SPACE: dict[str, Any] = {
    'space': {
        'id': '0',
        'name': 'alpha',
        'subnets': [
            {
                'cidr': '172.31.0.0/20',
                'provider-id': 'subnet-abc123',
                'provider-space-id': 'prov-space-1',
                'provider-network-id': 'vpc-123',
                'vlan-tag': 0,
                'zones': ['us-east-1a', 'us-east-1b'],
            },
            {
                'cidr': '10.0.0.0/24',
                'vlan-tag': 42,
                'zones': ['us-east-1a'],
            },
        ],
    },
    'applications': ['mysql', 'wordpress'],
    'machine-count': 3,
}

SHOW_SPACE_MINIMAL: dict[str, Any] = {
    'space': {
        'id': '2',
        'name': 'empty-space',
    },
    'applications': [],
    'machine-count': 0,
}
