import imgloader
from imgloader import ConfigDrawer


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


def test_adjust_text(monkeypatch):
    def mockreturn(mock_self):
        return None
    monkeypatch.setattr(ConfigDrawer, 'draw', mockreturn)

    drawer = ConfigDrawer('fake_canvas')

    drawer.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200)
    assert drawer.config['text']['id']['x'] == 100
    assert drawer.config['text']['id']['y'] == 200

    drawer.update_text(text_id='id', pos_x=400, pos_y=500)
    assert drawer.config['text']['id']['x'] == 400
    assert drawer.config['text']['id']['y'] == 500


def test_move_text(monkeypatch):
    def mockreturn(mock_self):
        return None
    monkeypatch.setattr(ConfigDrawer, 'draw', mockreturn)

    drawer = ConfigDrawer('fake_canvas')

    drawer.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200)
    assert drawer.config['text']['id']['x'] == 100
    assert drawer.config['text']['id']['y'] == 200

    drawer.move_text(text_id='id', move_x=400, move_y=-50)
    assert drawer.config['text']['id']['x'] == 500
    assert drawer.config['text']['id']['y'] == 150


def test_removed_text_from_config(monkeypatch):
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


def test_add_text_unsaved_changes(monkeypatch):
    def mockreturn(mock_self):
        return None
    monkeypatch.setattr(ConfigDrawer, 'draw', mockreturn)

    drawer = ConfigDrawer('fake_canvas')
    assert not drawer.unsaved_changes

    drawer.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200)
    assert drawer.unsaved_changes