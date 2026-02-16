import jubilant

from . import mocks


def test_name_only(run: mocks.Run):
    run.handle(['juju', 'add-space', 'my-space'])
    juju = jubilant.Juju()

    juju.add_space('my-space')


def test_with_cidrs(run: mocks.Run):
    run.handle(['juju', 'add-space', 'my-space', '172.31.0.0/20', '10.0.0.0/24'])
    juju = jubilant.Juju()

    juju.add_space('my-space', '172.31.0.0/20', '10.0.0.0/24')


def test_with_model(run: mocks.Run):
    run.handle(['juju', 'add-space', '--model', 'mdl', 'my-space'])
    juju = jubilant.Juju(model='mdl')

    juju.add_space('my-space')
