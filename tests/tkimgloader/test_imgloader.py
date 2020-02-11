
import builtins
import json

from imgloader import ConfigDrawer


def test_config_after_init():
    drawer = ConfigDrawer('fake_canvas')
    assert 'background' in drawer.config
    assert not drawer.config['background']
    assert 'text' in drawer.config
    assert not drawer.config['text']


def test_config_saved(monkeypatch):
    def mockreturn(mock_self):
        return None
    monkeypatch.setattr(ConfigDrawer, 'draw', mockreturn)

    drawer = ConfigDrawer('fake_canvas')
    test_config = {1: 'config'}

    drawer.config = test_config
    assert drawer.config == test_config


def test_background_set(monkeypatch):
    def mockreturn(mock_self):
        return None
    monkeypatch.setattr(ConfigDrawer, 'draw', mockreturn)

    drawer = ConfigDrawer('fake_canvas')
    drawer.background = 'my_path'
    assert drawer.config['background'] == 'my_path'


def test_text_added_in_config(monkeypatch):
    def mockreturn(mock_self):
        return None
    monkeypatch.setattr(ConfigDrawer, 'draw', mockreturn)

    drawer = ConfigDrawer('fake_canvas')

    drawer.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200)
    assert 'text' in drawer.config
    assert 'id' in drawer.config['text']
    assert drawer.config['text']['id']['text'] == 'sample_text'
    assert drawer.config['text']['id']['x'] == 100
    assert drawer.config['text']['id']['y'] == 200


def test_removed_from_config(monkeypatch):
    def mockreturn(mock_self):
        return None
    monkeypatch.setattr(ConfigDrawer, 'draw', mockreturn)

    drawer = ConfigDrawer('fake_canvas')

    drawer.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200)
    assert len(drawer.config['text']) == 1
    assert 'id' in drawer.config['text']

    drawer.remove_text(text_id='id')
    assert 'text' in drawer.config
    assert 'id' not in drawer.config['text']
