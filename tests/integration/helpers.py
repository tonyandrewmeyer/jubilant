from __future__ import annotations

import pathlib

CHARMS_PATH = pathlib.Path(__file__).parent / 'charms'

# Test SSH key pair - only for use in integration tests
TEST_SSH_PRIVATE_KEY = """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDBApPszf6ki9VNAWpAsU6VY1iM59qe5HyE08zr8tw0SgAAAKDNXMCLzVzA
iwAAAAtzc2gtZWQyNTUxOQAAACDBApPszf6ki9VNAWpAsU6VY1iM59qe5HyE08zr8tw0Sg
AAAEAVfiT1ThKA3424TcV06ftOd1agt6trEQfYrI6wfULvCsECk+zN/qSL1U0BakCxTpVj
WIzn2p7kfITTzOvy3DRKAAAAF3RhbWV5ZXJAdGFtLWNhbm9uY2lhbC0xAQIDBAUG
-----END OPENSSH PRIVATE KEY-----
"""

TEST_SSH_PUBLIC_KEY = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMECk+zN/qSL1U0BakCxTpVjWIzn2p7kfITTzOvy3DRK tameyer@tam-canoncial-1'


def find_charm(name: str) -> pathlib.Path:
    """Find given test charm and return absolute path to .charm file."""
    # .charm filename has platform in it, so search with *.charm
    charms = [p.absolute() for p in (CHARMS_PATH / name).glob('*.charm')]
    assert charms, f'{name} .charm file not found'
    assert len(charms) == 1, f'{name} has more than one .charm file, unsure which to use'
    return charms[0]
