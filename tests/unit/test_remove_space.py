import jubilant

from . import mocks


def test_defaults(run: mocks.Run):
    run.handle(['juju', 'remove-space', '--yes', 'myspace'])
    juju = jubilant.Juju()

    juju.remove_space('myspace')


def test_with_model(run: mocks.Run):
    run.handle(['juju', 'remove-space', '--model', 'mdl', '--yes', 'myspace'])
    juju = jubilant.Juju(model='mdl')

    juju.remove_space('myspace')


def test_force(run: mocks.Run):
    run.handle(['juju', 'remove-space', '--yes', 'myspace', '--force'])
    juju = jubilant.Juju()

    juju.remove_space('myspace', force=True)
