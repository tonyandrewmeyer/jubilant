from __future__ import annotations

import pathlib

CHARMS_PATH = pathlib.Path(__file__).parent / 'charms'

# Test SSH key pair - only for use in integration tests
TEST_SSH_PRIVATE_KEY = """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBnYWL2nF3Wq8cXMx/Jx7KJGvPJxZvCZqFGYZKxWqPJMAAAAJhqJF3MaiRd
zAAAAAtzc2gtZWQyNTUxOQAAACBnYWL2nF3Wq8cXMx/Jx7KJGvPJxZvCZqFGYZKxWqPJMA
AAAEDKQxXzN+xj7FvUqH3cNJzJfXGU3k5JH8cLQZ1fYGLRXGdhYvacXdarxxczH8nHsoka
88nFm8JmoUZhkrFao8kwAAAAFGp1YmlsYW50LXRlc3Qta2V5LTEBAgMEBQ==
-----END OPENSSH PRIVATE KEY-----
"""

TEST_SSH_PUBLIC_KEY = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGdhYvacXdarxxczH8nHsoka88nFm8JmoUZhkrFao8kw jubilant-test-key-1\n'


def find_charm(name: str) -> pathlib.Path:
    """Find given test charm and return absolute path to .charm file."""
    # .charm filename has platform in it, so search with *.charm
    charms = [p.absolute() for p in (CHARMS_PATH / name).glob('*.charm')]
    assert charms, f'{name} .charm file not found'
    assert len(charms) == 1, f'{name} has more than one .charm file, unsure which to use'
    return charms[0]
