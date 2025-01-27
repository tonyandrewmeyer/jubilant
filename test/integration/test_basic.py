import pytest

import jubilant


# NOTE: use jubilant.fixtures model/Juju fixture when ready, see:
# https://github.com/canonical/jubilant/issues/20
@pytest.fixture
def juju():
    j = jubilant.Juju()
    j.add_model('tt')
    yield j
    j.destroy_model('tt')


def test_deploy(juju: jubilant.Juju):
    juju.deploy('snappass-test')

    juju.wait(lambda status: status.apps['snappass-test'].is_active)
