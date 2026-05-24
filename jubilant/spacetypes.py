"""Dataclasses that contain parsed output from ``juju spaces`` and ``juju show-space``."""

from __future__ import annotations

import dataclasses
from typing import Any


@dataclasses.dataclass(frozen=True)
class SubnetInfo:
    """Information about a subnet in a space (from ``juju show-space``)."""

    cidr: str
    vlan_tag: int

    provider_id: str = ''
    provider_space_id: str = ''
    provider_network_id: str = ''
    zones: tuple[str, ...] = ()

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> SubnetInfo:
        return cls(
            cidr=d['cidr'],
            vlan_tag=d.get('vlan-tag', 0),
            provider_id=d.get('provider-id') or '',
            provider_space_id=d.get('provider-space-id') or '',
            provider_network_id=d.get('provider-network-id') or '',
            zones=tuple(d.get('zones') or ()),
        )


@dataclasses.dataclass(frozen=True)
class SpaceInfo:
    """Information about a space (from ``juju show-space``)."""

    id: str
    name: str

    subnets: tuple[SubnetInfo, ...] = ()

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> SpaceInfo:
        subnets_list: list[dict[str, Any]] = d.get('subnets') or []
        return cls(
            id=d['id'],
            name=d['name'],
            subnets=tuple(SubnetInfo._from_dict(s) for s in subnets_list),
        )


@dataclasses.dataclass(frozen=True)
class ShowSpaceInfo:
    """Parsed version of the object returned by ``juju show-space --format=json``."""

    space: SpaceInfo
    applications: tuple[str, ...] = ()
    machine_count: int = 0

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> ShowSpaceInfo:
        return cls(
            space=SpaceInfo._from_dict(d['space']),
            applications=tuple(d.get('applications') or []),
            machine_count=d.get('machine-count', 0),
        )


@dataclasses.dataclass(frozen=True)
class SpaceSubnet:
    """Information about a subnet in a space (from ``juju spaces``)."""

    type: str
    status: str
    zones: tuple[str, ...] = ()
    provider_id: str = ''

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> SpaceSubnet:
        return cls(
            type=d.get('type') or '',
            status=d.get('status') or '',
            zones=tuple(d.get('zones') or ()),
            provider_id=d.get('provider-id') or '',
        )


@dataclasses.dataclass(frozen=True)
class Space:
    """Parsed version of a single space from ``juju spaces --format=json``."""

    id: str
    name: str
    subnets: dict[str, SpaceSubnet] = dataclasses.field(default_factory=dict)  # type: ignore

    @classmethod
    def _from_dict(cls, d: dict[str, Any]) -> Space:
        subnets_dict: dict[str, Any] = d.get('subnets') or {}
        return cls(
            id=d['id'],
            name=d['name'],
            subnets={
                cidr: SpaceSubnet._from_dict(subnet) for cidr, subnet in subnets_dict.items()
            },
        )
