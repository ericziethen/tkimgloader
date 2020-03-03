
import copy

import pytest

import tkimgloader.imgloader as imgloader
from tkimgloader.imgloader import ConfigDrawer
from tkimgloader.widgets import Widget, WidgetCategory, WidgetType

def test_config_after_init():
    drawer = ConfigDrawer('fake_canvas')

    assert drawer.canvas == 'fake_canvas'
    assert not drawer.background_path
    assert not drawer.widgets


def test_load_background():
    drawer = ConfigDrawer('fake_canvas')

    assert not drawer.background_path
    drawer.load_background('path', redraw=False)
    assert drawer.background_path == 'path'


def test_init_no_unsaved_changes():
    drawer = ConfigDrawer('fake_canvas')

    assert not drawer.unsaved_changes


def test_load_config_no_unsaved_changed():
    config = {
        "background": "path",
        "text": {
            "key": {"text": "Test", "x": 100, "y": 100}
        }
    }

    drawer = ConfigDrawer('fake_canvas')
    drawer.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200, redraw=False)
    assert drawer.unsaved_changes

    drawer._load_config(config, config_path='path', redraw=False)
    assert not drawer.unsaved_changes


def test_save_config_no_unsaved_changes(monkeypatch):
    def mock_json_save(mock, mock2):
        None
    monkeypatch.setattr(imgloader, 'dump_json', mock_json_save)

    drawer = ConfigDrawer('fake_canvas')
    drawer.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200, redraw=False)
    assert drawer.unsaved_changes

    drawer.save_config_to_file('fake_path')
    assert not drawer.unsaved_changes


def test_equal_init():
    drawer1 = ConfigDrawer('fake_canvas')
    drawer2 = ConfigDrawer('fake_canvas')

    assert drawer1 == drawer2


def test_save_load_config_identical(monkeypatch):
    def mock_json_save(mock, mock2):
        None
    monkeypatch.setattr(imgloader, 'dump_json', mock_json_save)

    # Create 1 Config from Blank $ Confirm empty, Add Text, Add Buttons
    drawer1 = ConfigDrawer('fake_canvas')
    drawer1.load_background('path', redraw=False)
    drawer1.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200, redraw=False)
    drawer1.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1'], redraw=False)
    drawer1.add_image_button(button_id='butt2', pos_x=100, pos_y=200, orig_on_release=False, images=['path1', 'path2'], redraw=False)
    drawer1.next_button_image(button_id='butt2', redraw=False)

    # Save the Config
    drawer1.save_config_to_file('fake_path')

    # Copy the saved config
    config_copy = copy.deepcopy(drawer1.saved_img_config)
    assert 'id' in config_copy['text']
    assert 'butt1' in config_copy['image_buttons']

    # Create Config 2 & Confirm Empty
    drawer2 = ConfigDrawer('fake_canvas')
    assert 'id' not in drawer2.config['text']
    assert 'butt1' not in drawer2.config['image_buttons']

    # Load Config
    drawer2._load_config(config_copy, config_path='fake_path', redraw=False)

    print(drawer1.__dict__)
    print(drawer2.__dict__)
    print(config_copy)

    # Check both configs the same
    assert drawer1 == drawer2


def test_form_full_widget_id():
    widget_type = WidgetType.BUTTON
    button_id = 'My Button'

    assert imgloader._form_full_widget_id(button_id, widget_type) == WidgetType.BUTTON.value + '_' + button_id


def test_widget_exists():
    drawer = ConfigDrawer('fake_canvas')

    widget_type = WidgetType.BUTTON
    button_id = 'My Button'

    assert not drawer.contains_widget(button_id, widget_type)
