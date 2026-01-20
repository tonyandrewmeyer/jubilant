"""Integration tests for space commands.

Note: These tests require a cloud provider that supports network spaces (e.g., MAAS).
They may fail or be skipped on clouds that don't support spaces like LXD.
"""

from __future__ import annotations

import contextlib

import pytest

import jubilant


@pytest.mark.machine
def test_spaces_list(juju: jubilant.Juju):
    """Test listing spaces.

    This should work on all environments, though the list may be empty.
    """
    spaces = juju.spaces()
    # Should return a list, possibly empty
    assert isinstance(spaces, list)
    # If there are spaces, check they have the expected structure
    for space in spaces:
        assert isinstance(space.name, str)
        assert isinstance(space.subnets, list)


@pytest.mark.machine
def test_add_show_remove_space(juju: jubilant.Juju):
    """Test adding, showing, and removing a space.

    This test will be skipped if the cloud provider doesn't support spaces.
    """
    space_name = 'test-space-jubilant'

    try:
        # Add a space
        juju.add_space(space_name)

        # Show the space
        space = juju.show_space(space_name)
        assert space.name == space_name
        assert isinstance(space.subnets, list)

        # List spaces and verify it's there
        spaces = juju.spaces()
        space_names = [s.name for s in spaces]
        assert space_name in space_names

    except jubilant.CLIError as e:
        if 'not supported' in e.stderr.lower() or 'cannot manage' in e.stderr.lower():
            pytest.skip(f'Cloud provider does not support spaces: {e.stderr}')
        raise
    finally:
        # Clean up
        with contextlib.suppress(jubilant.CLIError):
            juju.remove_space(space_name)


@pytest.mark.machine
def test_rename_space(juju: jubilant.Juju):
    """Test renaming a space.

    This test will be skipped if the cloud provider doesn't support spaces.
    """
    old_name = 'test-space-old'
    new_name = 'test-space-new'

    try:
        # Add a space
        juju.add_space(old_name)

        # Rename the space
        juju.rename_space(old_name, new_name)

        # Verify the new name exists
        spaces = juju.spaces()
        space_names = [s.name for s in spaces]
        assert new_name in space_names
        assert old_name not in space_names

    except jubilant.CLIError as e:
        if 'not supported' in e.stderr.lower() or 'cannot manage' in e.stderr.lower():
            pytest.skip(f'Cloud provider does not support spaces: {e.stderr}')
        raise
    finally:
        # Clean up
        with contextlib.suppress(jubilant.CLIError):
            juju.remove_space(new_name)


@pytest.mark.machine
def test_reload_spaces(juju: jubilant.Juju):
    """Test reloading spaces.

    This should work on all environments that support spaces.
    """
    try:
        juju.reload_spaces()
    except jubilant.CLIError as e:
        if 'not supported' in e.stderr.lower() or 'cannot manage' in e.stderr.lower():
            pytest.skip(f'Cloud provider does not support spaces: {e.stderr}')
        raise
