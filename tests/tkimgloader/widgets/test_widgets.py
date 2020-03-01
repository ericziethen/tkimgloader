
import pytest

from tkimgloader.widgets import (
    ButtonType, CanvasText, CanvasImageButton, Widget,
    WidgetCategory, WidgetType
)

###############################
#### GENERIC WIDGET TESTS #####
###############################
def test_init_widget():
    widget = Widget(widget_id='id', widget_category=WidgetCategory.CANVAS, widget_type=WidgetType.TEXT, pos_x=100, pos_y=200)

    assert widget.id == 'id'
    assert widget.widget_category == WidgetCategory.CANVAS
    assert widget.widget_type == WidgetType.TEXT
    assert widget.pos_x == 100
    assert widget.pos_y == 200


def test_invalid_category():
    with pytest.raises(ValueError):
        Widget(widget_id='id', widget_category=None, widget_type=WidgetType.TEXT, pos_x=100, pos_y=200)


def test_invalid_widget_type():
    with pytest.raises(ValueError):
        Widget(widget_id='id', widget_category=WidgetCategory.CANVAS, widget_type=None, pos_x=100, pos_y=200)


############################
#### CANVAS TEXT TESTS #####
############################
def test_init_canvas_text_widgit():
    text = CanvasText(text_id='id', pos_x=100, pos_y=200)

    assert text.id == 'id'
    assert text.widget_category == WidgetCategory.CANVAS
    assert text.widget_type == WidgetType.TEXT
    assert text.pos_x == 100
    assert text.pos_y == 200


####################################
#### CANVAS IMAGE BUTTON TESTS #####
####################################
def test_init_canvas_image_button():
    button = CanvasImageButton(button_id='id', button_type=ButtonType.RELEASE, pos_x=100, pos_y=200)

    assert button.id == 'id'
    assert button.button_type == ButtonType.RELEASE
    assert button.widget_category == WidgetCategory.CANVAS
    assert button.widget_type == WidgetType.BUTTON
    assert button.pos_x == 100
    assert button.pos_y == 200


def test_canvas_image_button_invalid_button_type():
    with pytest.raises(ValueError):
        CanvasImageButton(button_id='id', button_type=None, pos_x=100, pos_y=200)
