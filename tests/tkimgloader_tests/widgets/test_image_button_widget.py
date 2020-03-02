
import pytest

from tkimgloader.widgets import (
    ButtonType, CanvasImageButton, WidgetCategory, WidgetType
)

def test_init():
    button = CanvasImageButton(button_id='id', button_type=ButtonType.RELEASE, pos_x=100, pos_y=200)

    assert button.id == 'id'
    assert button.button_type == ButtonType.RELEASE
    assert button.widget_category == WidgetCategory.CANVAS
    assert button.widget_type == WidgetType.BUTTON
    assert button.pos_x == 100
    assert button.pos_y == 200


def test_init_invalid_button_type():
    with pytest.raises(ValueError):
        CanvasImageButton(button_id='id', button_type=None, pos_x=100, pos_y=200)


def test_move_to():
    button = CanvasImageButton(button_id='id', button_type=ButtonType.RELEASE, pos_x=100, pos_y=200)

    assert button.pos_x == 100
    assert button.pos_y == 200

    button.move_to(pos_x=300, pos_y=250)
    assert button.pos_x == 300
    assert button.pos_y == 250


def test_move_by():
    button = CanvasImageButton(button_id='id', button_type=ButtonType.RELEASE, pos_x=100, pos_y=200)

    assert button.pos_x == 100
    assert button.pos_y == 200

    button.move_by(move_x=25, move_y=-50)
    assert button.pos_x == 125
    assert button.pos_y == 150
