
import pytest

from tkimgloader.widgets import (
    Widget, WidgetCategory, WidgetType
)

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


def test_move_to():
    widget = Widget(widget_id='id', widget_category=WidgetCategory.CANVAS, widget_type=WidgetType.TEXT, pos_x=100, pos_y=200)

    assert widget.pos_x == 100
    assert widget.pos_y == 200

    widget.move_to(pos_x=300, pos_y=250)
    assert widget.pos_x == 300
    assert widget.pos_y == 250


def test_move_by():
    widget = Widget(widget_id='id', widget_category=WidgetCategory.CANVAS, widget_type=WidgetType.TEXT, pos_x=100, pos_y=200)

    assert widget.pos_x == 100
    assert widget.pos_y == 200

    widget.move_by(x=25, y=-50)
    assert widget.pos_x == 125
    assert widget.pos_y == 150
