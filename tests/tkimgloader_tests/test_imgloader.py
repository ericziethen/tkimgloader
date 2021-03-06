
import copy

import pytest

import tkimgloader.imgloader as imgloader
from tkimgloader.imgloader import ConfigDrawer


def test_add_widget():
    drawer = ConfigDrawer('fake_canvas')

    widget = drawer.add_text(text='myText', pos_x=200, pos_y=300, draw=False)
    assert id(widget) in drawer.widgets


def test_remove_widget():
    drawer = ConfigDrawer('fake_canvas')

    widget = drawer.add_text(text='myText', pos_x=200, pos_y=300, draw=False)
    widget_id = id(widget)

    assert widget_id in drawer.widgets

    drawer.remove_widget(widget, draw=False)
    assert widget_id not in drawer.widgets


def test_add_text_widget_duplicate_text():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_text(text='myText', pos_x=200, pos_y=300, draw=False)
    drawer.add_text(text='myText', pos_x=200, pos_y=300, draw=False)


def test_add_text_widget_with_label():
    drawer = ConfigDrawer('fake_canvas')

    widget = drawer.add_text(label='unique_label', text='myText', pos_x=200, pos_y=300, draw=False)
    assert widget.label == 'unique_label'



def test_add_input_box_widgetwith_label():
    drawer = ConfigDrawer('fake_canvas')

    widget = drawer.add_input_box(label='unique_label', pos_x=200, pos_y=300, draw=False)
    assert widget.label == 'unique_label'


def test_get_widget_with_label():
    drawer = ConfigDrawer('fake_canvas')

    assert not drawer.get_widget_with_label('myLabel')

    widget = drawer.add_input_box(label='myLabel', pos_x=200, pos_y=300, draw=False)
    assert drawer.get_widget_with_label('myLabel') == widget


def test_add_widgets_reject_duplicate_labels():
    drawer = ConfigDrawer('fake_canvas')

    widget = drawer.add_text(label='unique_label', text='myText', pos_x=200, pos_y=300, draw=False)
    with pytest.raises(ValueError):
        drawer.add_text(label='unique_label', text='myText', pos_x=200, pos_y=300, draw=False)



def test_config_after_init():
    drawer = ConfigDrawer('fake_canvas')

    assert drawer.canvas == 'fake_canvas'
    assert not drawer.background_path
    assert not drawer.widgets


def test_load_background():
    drawer = ConfigDrawer('fake_canvas')

    assert not drawer.background_path
    drawer.load_background('path', draw=False)
    assert drawer.background_path == 'path'


def test_init_no_unsaved_changes():
    drawer = ConfigDrawer('fake_canvas')

    assert not drawer.unsaved_changes


def test_load_config_no_unsaved_changed():
    config = {
        "background": "path",
        "Text": [
            {'label': None, "text": "Test", "x": 100, "y": 100}
        ]
    }

    drawer = ConfigDrawer('fake_canvas')
    drawer.add_text(text='sample_text', pos_x=100, pos_y=200, draw=False)
    assert drawer.unsaved_changes

    drawer._load_config(config, config_path='path', draw=False)
    assert not drawer.unsaved_changes


def test_save_config_no_unsaved_changes(monkeypatch):
    def mock_json_save(mock, mock2):
        None
    monkeypatch.setattr(imgloader, 'dump_json', mock_json_save)

    drawer = ConfigDrawer('fake_canvas')
    drawer.add_text(text='sample_text', pos_x=100, pos_y=200, draw=False)
    assert drawer.unsaved_changes

    drawer.save_config_to_file('fake_path')
    assert not drawer.unsaved_changes


def test_equal_init():
    drawer1 = ConfigDrawer('fake_canvas')
    drawer2 = ConfigDrawer('fake_canvas')

    assert drawer1 == drawer2


def test_equal_background():
    drawer1 = ConfigDrawer('fake_canvas')
    drawer2 = ConfigDrawer('fake_canvas')

    drawer1.load_background('path', draw=False)
    drawer2.load_background('path', draw=False)

    assert drawer1 == drawer2


def test_unequal_different_background():
    drawer1 = ConfigDrawer('fake_canvas')
    drawer2 = ConfigDrawer('fake_canvas')

    drawer1.load_background('path', draw=False)

    assert drawer1 != drawer2


def test_equal_same_text():
    drawer1 = ConfigDrawer('fake_canvas')
    drawer2 = ConfigDrawer('fake_canvas')

    drawer1.add_text(text='sample_text', pos_x=100, pos_y=200, draw=False)
    drawer2.add_text(text='sample_text', pos_x=100, pos_y=200, draw=False)

    assert drawer1 == drawer2


def test_unequal_different_text():
    drawer1 = ConfigDrawer('fake_canvas')
    drawer2 = ConfigDrawer('fake_canvas')
    drawer3 = ConfigDrawer('fake_canvas')
    drawer4 = ConfigDrawer('fake_canvas')

    drawer1.add_text(text='sample_text', pos_x=100, pos_y=200, draw=False)
    assert drawer1 != drawer2

    drawer2.add_text(text='sample_text2', pos_x=100, pos_y=200, draw=False)
    assert drawer1 != drawer2

    drawer3.add_text(text='sample_text', pos_x=300, pos_y=200, draw=False)
    assert drawer1 != drawer3

    drawer4.add_text(text='sample_text', pos_x=100, pos_y=400, draw=False)
    assert drawer1 != drawer4


def test_equal_same_button():
    drawer1 = ConfigDrawer('fake_canvas')
    drawer2 = ConfigDrawer('fake_canvas')

    drawer1.add_image_button(pos_x=100, pos_y=200, orig_on_release=True, images=['path1'], draw=False)
    drawer2.add_image_button(pos_x=100, pos_y=200, orig_on_release=True, images=['path1'], draw=False)
 
    assert drawer1 == drawer2


def test_unequal_different_button():
    drawer1 = ConfigDrawer('fake_canvas')
    drawer2 = ConfigDrawer('fake_canvas')
    drawer3 = ConfigDrawer('fake_canvas')
    drawer4 = ConfigDrawer('fake_canvas')
    drawer5 = ConfigDrawer('fake_canvas')

    drawer1.add_image_button(pos_x=100, pos_y=200, orig_on_release=True, images=['path1'], draw=False)
    assert drawer1 != drawer2

    drawer2.add_image_button(pos_x=2100, pos_y=200, orig_on_release=True, images=['path1'], draw=False)
    assert drawer1 != drawer2

    drawer3.add_image_button(pos_x=100, pos_y=300, orig_on_release=True, images=['path1'], draw=False)
    assert drawer1 != drawer3

    drawer4.add_image_button(pos_x=100, pos_y=200, orig_on_release=False, images=['path1'], draw=False)
    assert drawer1 != drawer4

    drawer5.add_image_button(pos_x=100, pos_y=200, orig_on_release=True, images=['path2'], draw=False)
    assert drawer1 != drawer5


def test_equal_same_multiple_widgets():
    drawer1 = ConfigDrawer('fake_canvas')
    drawer2 = ConfigDrawer('fake_canvas')

    drawer1.add_image_button(pos_x=100, pos_y=200, orig_on_release=True, images=['path1'], draw=False)
    drawer2.add_image_button(pos_x=100, pos_y=200, orig_on_release=True, images=['path1'], draw=False)

    drawer1.add_text(text='sample_text', pos_x=100, pos_y=200, draw=False)
    drawer2.add_text(text='sample_text', pos_x=100, pos_y=200, draw=False)

    assert drawer1 == drawer2


def test_save_load_config_identical(monkeypatch):
    def mock_json_save(mock, mock2):
        None
    monkeypatch.setattr(imgloader, 'dump_json', mock_json_save)

    # Create 1 Config from Blank $ Confirm empty, Add Text, Add Buttons
    drawer1 = ConfigDrawer('fake_canvas')
    drawer1.load_background('path', draw=False)

    # Add all widgets
    drawer1.add_text(label='myText', text='sample_text', pos_x=100, pos_y=200, draw=False)
    drawer1.add_image_button(label='button', pos_x=100, pos_y=200, orig_on_release=True, images=['path1'], draw=False)
    drawer1.add_input_box(label='box', pos_x=100, pos_y=200, draw=False)

    button2 = drawer1.add_image_button(pos_x=100, pos_y=200, orig_on_release=False, images=['path1', 'path2'], draw=False)
    button2.next_image()

    # Save the Config
    drawer1.save_config_to_file('fake_path')

    # Copy the saved config
    config_copy = copy.deepcopy(drawer1.saved_img_config)

    # Create Config 2 & Confirm Empty
    drawer2 = ConfigDrawer('fake_canvas')
    d2_config = drawer2.calc_config_dict()

    # Load Config
    drawer2._load_config(config_copy, config_path='fake_path', draw=False)

    # Check can find our Label
    widget = drawer2.get_widget_with_label('myText')
    assert widget is not None

    print(drawer1.calc_config_dict())
    print(drawer2.calc_config_dict())

    # Check both configs the same
    assert drawer1 == drawer2
