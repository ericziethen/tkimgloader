
import imgloader
from imgloader import ConfigDrawer

def test_config_after_init():
    drawer = ConfigDrawer('fake_canvas')

    assert 'background' in drawer.config
    assert not drawer.config['background']
    assert 'text' in drawer.config
    assert not drawer.config['text']


def test_init_no_unsaved_changes():
    drawer = ConfigDrawer('fake_canvas')

    assert not drawer.unsaved_changes


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





def test_load_config_no_unsaved_changed(monkeypatch):
    def mockreturn(mock_self):
        return None
    monkeypatch.setattr(ConfigDrawer, 'draw', mockreturn)

    def mock_json_load(mock):
        return {"background": "path","text": {
                "key": {"text": "Test", "x": 100, "y": 100}}}
    monkeypatch.setattr(imgloader, 'load_json', mock_json_load)

    drawer = ConfigDrawer('fake_canvas')
    drawer.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200)
    assert drawer.unsaved_changes

    drawer.load_config('fake_path')
    assert not drawer.unsaved_changes


def test_save_config_no_unsaved_changes(monkeypatch):
    def mockreturn(mock_self):
        return None
    monkeypatch.setattr(ConfigDrawer, 'draw', mockreturn)

    def mock_json_save(mock, mock2):
        None
    monkeypatch.setattr(imgloader, 'dump_json', mock_json_save)

    drawer = ConfigDrawer('fake_canvas')
    drawer.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200)
    assert drawer.unsaved_changes

    drawer.save_config('fake_path')
    assert not drawer.unsaved_changes
