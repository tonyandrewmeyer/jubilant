import jubilant

from . import mocks


def test_name_only(run: mocks.Run):
    run.handle(['juju', 'add-space', 'myspace'])
    juju = jubilant.Juju()

    juju.add_space('myspace')


def test_with_model(run: mocks.Run):
    run.handle(['juju', 'add-space', '--model', 'mdl', 'myspace'])
    juju = jubilant.Juju(model='mdl')

    juju.add_space('myspace')


def test_with_cidrs(run: mocks.Run):
    run.handle(['juju', 'add-space', 'myspace', '172.31.0.0/20', '10.0.0.0/8'])
    juju = jubilant.Juju()

    juju.add_space('myspace', '172.31.0.0/20', '10.0.0.0/8')
