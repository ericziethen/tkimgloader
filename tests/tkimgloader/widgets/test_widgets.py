
import pytest

from tkimgloader.widgets import Widget, WidgetCategory, WidgetType


def test_init():
    widget = Widget(widget_id='id', widget_category=WidgetCategory.CANVAS, widget_type=WidgetType.TEXT, pos_x=100, pos_y=200)

    assert widget.id == 'id'
    assert widget.category == WidgetCategory.CANVAS
    assert widget.type == WidgetType.TEXT
    assert widget.pos_x == 100
    assert widget.pos_y == 200


def test_invalid_category():
    with pytest.raises(ValueError):
        Widget(widget_id='id', widget_category=None, widget_type=WidgetType.TEXT, pos_x=100, pos_y=200)


def test_invalid_widget_type():
    with pytest.raises(ValueError):
        Widget(widget_id='id', widget_category=WidgetCategory.CANVAS, widget_type=None, pos_x=100, pos_y=200)
