
import pytest

from imgloader import ConfigDrawer
from tkimgloader.widgets import WidgetType


def test_add_text():
    drawer = ConfigDrawer('fake_canvas')
    assert not drawer.widgets

    widget = drawer.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200, redraw=False)

    assert drawer.contains_widget('id', WidgetType.TEXT)
    assert widget.text == 'sample_text'


def test_add_widget_duplicate_id():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200, redraw=False)

    with pytest.raises(ValueError):
        drawer.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200, redraw=False)


def test_removed_text_from_config():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200, redraw=False)
    assert drawer.contains_widget('id', WidgetType.TEXT)

    drawer.remove_text(text_id='id', redraw=False)
    assert not drawer.widgets


def test_add_text_unsaved_changes():

    drawer = ConfigDrawer('fake_canvas')
    assert not drawer.unsaved_changes

    drawer.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200, redraw=False)
    assert drawer.unsaved_changes


def test_equal_text():
    drawer1 = ConfigDrawer('fake_canvas')
    drawer2 = ConfigDrawer('fake_canvas')

    drawer1.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200, redraw=False)
    drawer2.add_text(text_id='id', text='sample_text', pos_x=100, pos_y=200, redraw=False)

    assert drawer1 == drawer2
