
import pytest

from tkimgloader.widgets import (
    CanvasText, WidgetCategory, WidgetType
)


def test_init():
    text = CanvasText(text_id='id', text='my text', pos_x=100, pos_y=200)

    assert text.id == 'id'
    assert text.text == 'my text'
    assert text.widget_category == WidgetCategory.CANVAS
    assert text.widget_type == WidgetType.TEXT
    assert text.pos_x == 100
    assert text.pos_y == 200


def test_move_to():
    text = CanvasText(text_id='id', text='my text', pos_x=100, pos_y=200)

    assert text.pos_x == 100
    assert text.pos_y == 200

    text.move_to(pos_x=300, pos_y=250)
    assert text.pos_x == 300
    assert text.pos_y == 250


def test_move_by():
    text = CanvasText(text_id='id', text='my text', pos_x=100, pos_y=200)

    assert text.pos_x == 100
    assert text.pos_y == 200

    text.move_by(x=25, y=-50)
    assert text.pos_x == 125
    assert text.pos_y == 150
