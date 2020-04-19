
import pytest

from tkimgloader.widgets import (
    CanvasTable, CanvasText, CanvasImageButton, ButtonType, WidgetType
)


def test_create_widget():
    table = CanvasTable(
        label='table1', pos_x=100, pos_y=200,
        column_widths=(50, 100, 100),
        row_heights=(100, 200)
    )

    assert table.label == 'table1'
    assert table.widget_type == WidgetType.TABLE
    assert table.pos_x == 100
    assert table.pos_y == 200

    assert table.get_widget(col=1, row=1) is None
    assert table.get_widget(col=1, row=2) is None
    assert table.get_widget(col=2, row=1) is None
    assert table.get_widget(col=2, row=2) is None
    assert table.get_widget(col=3, row=1) is None
    assert table.get_widget(col=3, row=2) is None


def test_widget_str():
    widget = CanvasTable(label='table1', pos_x=50, pos_y=300, column_widths=[], row_heights=[])

    assert str(widget) == '(Table) [table1][50,300]'


def test_move_to():
    widget = CanvasTable(label='table1', pos_x=50, pos_y=300, column_widths=[], row_heights=[])

    assert widget.pos_x == 50
    assert widget.pos_y == 300

    widget.move_to(pos_x=800, pos_y=600)
    assert widget.pos_x == 800
    assert widget.pos_y == 600


def test_move_by():
    widget = CanvasTable(label='table1', pos_x=50, pos_y=300, column_widths=[], row_heights=[])

    assert widget.pos_x == 50
    assert widget.pos_y == 300

    widget.move_by(move_x=100, move_y=-120)
    assert widget.pos_x == 150
    assert widget.pos_y == 180


def test_add_widget():
    table = CanvasTable(label='table1', pos_x=50, pos_y=300, column_widths=[10, 20], row_heights=[10])

    assert table.get_widget(col=1, row=1) is None
    assert table.get_widget(col=2, row=1) is None

    text_widget = CanvasText(text='myText', pos_x=200, pos_y=300)
    table.add_widget(text_widget, row=1, col=1)

    img_widget = CanvasImageButton(
        button_type=ButtonType.RELEASE, pos_x=200, pos_y=300,
        image_list=['path1'])
    table.add_widget(img_widget, row=1, col=2)

    assert table.get_widget(col=1, row=1) == text_widget
    assert table.get_widget(col=2, row=1) == img_widget


def test_add_widget_unsupported_widget():
    table = CanvasTable(label='table1', pos_x=50, pos_y=300, column_widths=[10], row_heights=[10])

    table2 = CanvasTable(label='table2', pos_x=50, pos_y=300, column_widths=[10], row_heights=[10])
    with pytest.raises(ValueError):
        table.add_widget(table2, col=1, row=1)

'''

def test_add_widget_invalid_row():
    assert False

def test_add_widget_invalid_column():
    assert False

def test_add_widget_calc_position():
    assert False





def test_remove_widget():
    assert False

def test_add_row():
    assert False

def test_remove_row():
    assert False

def test_set_row_width():
    assert False

def test_add_column():
    assert False

def test_remove_column():
    assert False

def test_widget_to_dict():
    assert False

def test_set_column_width():
    assert False


def test_me_good():
    assert False
    # TODO
    # ADD IMGLOADER TESTS FOR THIS CLASS
'''
