import jubilant

from . import mocks


def test_rename(run: mocks.Run):
    run.handle(['juju', 'rename-space', 'old-name', 'new-name'])
    juju = jubilant.Juju()

    juju.rename_space('old-name', 'new-name')


def test_with_model(run: mocks.Run):
    run.handle(['juju', 'rename-space', '--model', 'mdl', 'old-name', 'new-name'])
    juju = jubilant.Juju(model='mdl')

    juju.rename_space('old-name', 'new-name')
