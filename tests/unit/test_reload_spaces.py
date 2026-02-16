import jubilant

from . import mocks


def test_defaults(run: mocks.Run):
    run.handle(['juju', 'reload-spaces'])
    juju = jubilant.Juju()

    juju.reload_spaces()


def test_with_model(run: mocks.Run):
    run.handle(['juju', 'reload-spaces', '--model', 'mdl'])
    juju = jubilant.Juju(model='mdl')

    juju.reload_spaces()
