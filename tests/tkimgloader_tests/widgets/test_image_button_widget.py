
import pytest
from PIL import ImageTk


from tkimgloader.widgets import (
    ButtonType, CanvasImageButton, WidgetType
)


def test_create_widget():
    widget = CanvasImageButton(
        button_id='myButton', button_type=ButtonType.RELEASE, pos_x=100, pos_y=200,
        image_list=['path1', 'path2', 'path3'], current_image=3)

    assert widget.id == 'myButton'
    assert widget.widget_type == WidgetType.BUTTON
    assert widget.pos_x == 100
    assert widget.pos_y == 200

    assert widget.button_type == ButtonType.RELEASE
    assert widget.image_path_dic == {1: 'path1', 2: 'path2', 3: 'path3'}
    assert widget.current_image == 3


def test_widget_str():
    widget = CanvasImageButton(
        button_id='myButton', button_type=ButtonType.RELEASE, pos_x=100, pos_y=200,
        image_list=['path1', 'path2', 'path3'], current_image=3)

    assert str(widget) == 'myButton [100,200]'


def test_widget_to_dict():
    widget = CanvasImageButton(
        button_id='myButton', button_type=ButtonType.RELEASE, pos_x=100, pos_y=200,
        image_list=['path1', 'path2', 'path3'], current_image=3)

    assert widget.to_dict() == {
        'x': 100,
        'y': 200,
        'orig_image_on_release': True,
        'current_image': 3,
        'images': {
            1: 'path1',
            2: 'path2',
            3: 'path3'
        }
    }

def test_move_to():
    widget = CanvasImageButton(
        button_id='myButton', button_type=ButtonType.RELEASE, pos_x=100, pos_y=200,
        image_list=['path1', 'path2', 'path3'], current_image=3)
    assert widget.pos_x == 100
    assert widget.pos_y == 200

    widget.move_to(pos_x=800, pos_y=600)
    assert widget.pos_x == 800
    assert widget.pos_y == 600


def test_move_by():
    widget = CanvasImageButton(
        button_id='myButton', button_type=ButtonType.RELEASE, pos_x=200, pos_y=300,
        image_list=['path1', 'path2', 'path3'], current_image=3)
    assert widget.pos_x == 200
    assert widget.pos_y == 300

    widget.move_by(move_x=-50, move_y=150)
    assert widget.pos_x == 150
    assert widget.pos_y == 450


def test_next_image():
    widget = CanvasImageButton(
        button_id='myButton', button_type=ButtonType.RELEASE, pos_x=200, pos_y=300,
        image_list=['path1', 'path2', 'path3'], current_image=3)
    assert widget.current_image == 3

    widget.next_image()
    assert widget.current_image == 1

    widget.next_image()
    assert widget.current_image == 2

    widget.next_image()
    assert widget.current_image == 3


def test_previous_image():
    widget = CanvasImageButton(
        button_id='myButton', button_type=ButtonType.RELEASE, pos_x=200, pos_y=300,
        image_list=['path1', 'path2', 'path3'], current_image=3)
    assert widget.current_image == 3

    widget.previous_image()
    assert widget.current_image == 2

    widget.previous_image()
    assert widget.current_image == 1

    widget.previous_image()
    assert widget.current_image == 3


def test_add_new_images(monkeypatch):
    def mock_photo_image(*args, **kwargs):
        return None
    monkeypatch.setattr(ImageTk, 'PhotoImage', mock_photo_image)

    widget = CanvasImageButton(
        button_id='myButton', button_type=ButtonType.RELEASE, pos_x=200, pos_y=300,
        image_list=['path1'])
    assert len(widget.image_path_dic) == 1
    assert widget.current_image == 1

    widget.add_new_images(['path2', 'path4'])
    assert len(widget.image_path_dic) == 3
    assert widget.current_image == 2
    assert widget.image_path_dic[1] == 'path1'
    assert widget.image_path_dic[2] == 'path2'
    assert widget.image_path_dic[3] == 'path4'

    widget.add_new_images(['path3'])
    assert len(widget.image_path_dic) == 4
    assert widget.current_image == 3
    assert widget.image_path_dic[1] == 'path1'
    assert widget.image_path_dic[2] == 'path2'
    assert widget.image_path_dic[3] == 'path3'
    assert widget.image_path_dic[4] == 'path4'


def test_remove_current_image():
    widget = CanvasImageButton(
        button_id='myButton', button_type=ButtonType.RELEASE, pos_x=200, pos_y=300,
        image_list=['path1', 'path2', 'path3'], current_image=2)
    assert len(widget.image_path_dic) == 3
    assert widget.current_image == 2
    assert widget.image_path_dic[1] == 'path1'
    assert widget.image_path_dic[2] == 'path2'
    assert widget.image_path_dic[3] == 'path3'

    widget.remove_current_image()
    assert len(widget.image_path_dic) == 2
    assert widget.current_image == 1
    assert widget.image_path_dic[1] == 'path1'
    assert widget.image_path_dic[2] == 'path3'

    widget.remove_current_image()
    assert len(widget.image_path_dic) == 1
    assert widget.current_image == 1
    assert widget.image_path_dic[1] == 'path3'


def test_remove_current_image_last_image():
    widget = CanvasImageButton(
        button_id='myButton', button_type=ButtonType.RELEASE, pos_x=200, pos_y=300,
        image_list=['path1'])

    with pytest.raises(ValueError):
        widget.remove_current_image()
