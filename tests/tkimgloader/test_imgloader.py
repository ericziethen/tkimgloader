
from imgloader import ConfigDrawer

def test_config_saved(monkeypatch):
    def mockreturn(mock_self):
        return None
    monkeypatch.setattr(ConfigDrawer, 'draw', mockreturn)

    drawer = ConfigDrawer('fake_canvas')
    test_config = {1: 'config'}

    assert not drawer.config
    drawer.config = test_config
    assert drawer.config == test_config




