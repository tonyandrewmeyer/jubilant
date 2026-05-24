import jubilant

from . import mocks


def test_defaults(run: mocks.Run):
    run.handle(['juju', 'remove-space', '--yes', 'my-space'])
    juju = jubilant.Juju()

    juju.remove_space('my-space')


def test_force(run: mocks.Run):
    run.handle(['juju', 'remove-space', '--yes', 'my-space', '--force'])
    juju = jubilant.Juju()

    juju.remove_space('my-space', force=True)


def test_with_model(run: mocks.Run):
    run.handle(['juju', 'remove-space', '--model', 'mdl', '--yes', 'my-space'])
    juju = jubilant.Juju(model='mdl')

    juju.remove_space('my-space')
