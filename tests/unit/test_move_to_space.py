import jubilant

from . import mocks


def test_move(run: mocks.Run):
    run.handle(['juju', 'move-to-space', 'db-space', '172.31.0.0/20'])
    juju = jubilant.Juju()

    juju.move_to_space('db-space', '172.31.0.0/20')


def test_multiple_cidrs(run: mocks.Run):
    run.handle(['juju', 'move-to-space', 'db-space', '172.31.0.0/20', '10.0.0.0/24'])
    juju = jubilant.Juju()

    juju.move_to_space('db-space', '172.31.0.0/20', '10.0.0.0/24')


def test_force(run: mocks.Run):
    run.handle(['juju', 'move-to-space', 'db-space', '172.31.0.0/20', '--force'])
    juju = jubilant.Juju()

    juju.move_to_space('db-space', '172.31.0.0/20', force=True)


def test_with_model(run: mocks.Run):
    run.handle(['juju', 'move-to-space', '--model', 'mdl', 'db-space', '172.31.0.0/20'])
    juju = jubilant.Juju(model='mdl')

    juju.move_to_space('db-space', '172.31.0.0/20')
