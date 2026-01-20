"""Dataclasses that contain parsed output from juju spaces commands."""

from __future__ import annotations

import dataclasses
from typing import Any


@dataclasses.dataclass(frozen=True)
class Space:
    """Represents a network space."""

    name: str
    subnets: list[Subnet]

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> Space:
        subnets_data = d.get('subnets', [])
        # Handle both simple string subnets and complex subnet objects
        if len(subnets_data) > 0 and isinstance(subnets_data[0], str):
            subnets = [Subnet(cidr=cidr) for cidr in subnets_data]
        elif len(subnets_data) > 0:
            subnets = [Subnet._from_dict(subnet) for subnet in subnets_data]
        else:
            subnets = []
        return Space(
            name=d['name'],
            subnets=subnets,
        )


@dataclasses.dataclass(frozen=True)
class Subnet:
    """Represents a subnet in a network space."""

    cidr: str
    provider_id: str | None = None
    provider_space_id: str | None = None
    provider_network_id: str | None = None
    vlan_tag: int | None = None
    zones: list[str] | None = None

    @classmethod
    def _from_dict(cls, d: dict[str, Any] | str) -> Subnet:
        # Handle simple string case (just CIDR)
        if isinstance(d, str):
            return Subnet(cidr=d)
        # Handle full object
        return Subnet(
            cidr=d['cidr'],
            provider_id=d.get('provider-id'),
            provider_space_id=d.get('provider-space-id'),
            provider_network_id=d.get('provider-network-id'),
            vlan_tag=d.get('vlan-tag'),
            zones=d.get('zones'),
        )
