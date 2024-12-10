import pytest

import jubilant


@pytest.fixture
def juju():
    j = jubilant.Juju()
    j.add_model('tt')  # TODO: random model name
    yield j
    j.destroy_model('tt')


def test_deploy(juju):
    juju.deploy('snappass-test')

    def is_active(status):
        return status.applications['snappass-test'].application_status.current == 'active'

    juju.wait_status(is_active)
