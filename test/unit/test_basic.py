import jubilant


def test_repr():
    juju = jubilant.Juju()
    assert repr(juju) == 'Juju()'
