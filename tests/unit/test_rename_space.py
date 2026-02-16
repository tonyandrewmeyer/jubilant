import jubilant

from . import mocks


def test_defaults(run: mocks.Run):
    run.handle(['juju', 'rename-space', 'old', 'new'])
    juju = jubilant.Juju()

    juju.rename_space('old', 'new')


def test_with_model(run: mocks.Run):
    run.handle(['juju', 'rename-space', '--model', 'mdl', 'old', 'new'])
    juju = jubilant.Juju(model='mdl')

    juju.rename_space('old', 'new')
