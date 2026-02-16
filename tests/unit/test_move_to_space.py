import jubilant

from . import mocks


def test_defaults(run: mocks.Run):
    run.handle(['juju', 'move-to-space', 'myspace', '172.31.1.0/28'])
    juju = jubilant.Juju()

    juju.move_to_space('myspace', '172.31.1.0/28')


def test_with_model(run: mocks.Run):
    run.handle(['juju', 'move-to-space', '--model', 'mdl', 'myspace', '172.31.1.0/28'])
    juju = jubilant.Juju(model='mdl')

    juju.move_to_space('myspace', '172.31.1.0/28')


def test_multiple_cidrs(run: mocks.Run):
    run.handle(['juju', 'move-to-space', 'myspace', '172.31.1.0/28', '172.31.16.0/20'])
    juju = jubilant.Juju()

    juju.move_to_space('myspace', '172.31.1.0/28', '172.31.16.0/20')


def test_force(run: mocks.Run):
    run.handle(['juju', 'move-to-space', 'myspace', '172.31.1.0/28', '--force'])
    juju = jubilant.Juju()

    juju.move_to_space('myspace', '172.31.1.0/28', force=True)
