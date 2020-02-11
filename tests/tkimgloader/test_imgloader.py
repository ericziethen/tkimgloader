
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


def test_text_added_in_config():
    drawer = ConfigDrawer('fake_canvas')
    
    assert not drawer.config

    drawer.add_text(text_id='id', text='sample_text', x=100, y=200)
    assert 'text' in drawer.config
    assert 'id' in drawer.config['text']
    assert drawer.config['text']['id']['text'] == 'sample_text'
    assert drawer.config['text']['id']['x'] == 100
    assert drawer.config['text']['id']['y'] == 200

# def text_removed_from_config():
