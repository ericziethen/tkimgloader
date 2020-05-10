
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


def test_add_widget_invalid_index():
    table = CanvasTable(label='table1', pos_x=50, pos_y=300, column_widths=[10], row_heights=[10])

    text_widget = CanvasText(text='myText', pos_x=200, pos_y=300)
    with pytest.raises(IndexError):
        table.add_widget(text_widget, col=0, row=1)

    with pytest.raises(IndexError):
        table.add_widget(text_widget, col=1, row=0)

    with pytest.raises(IndexError):
        table.add_widget(text_widget, col=2, row=1)

    with pytest.raises(IndexError):
        table.add_widget(text_widget, col=1, row=2)

    table.add_widget(text_widget, col=1, row=1)


def test_get_widget_invalid_index():
    table = CanvasTable(label='table1', pos_x=50, pos_y=300, column_widths=[5, 4, 3], row_heights=[5, 1, 2])

    with pytest.raises(IndexError):
        table.get_widget(col=0, row=1)

    with pytest.raises(IndexError):
        table.get_widget(col=1, row=0)

    with pytest.raises(IndexError):
        table.get_widget(col=4, row=3)

    with pytest.raises(IndexError):
        table.get_widget(col=3, row=4)


def test_remove_widget():
    table = CanvasTable(label='table1', pos_x=50, pos_y=300, column_widths=[5, 4, 3], row_heights=[5, 1, 2])
    text_widget = CanvasText(text='myText', pos_x=200, pos_y=300)

    assert table.get_widget(col=1, row=2) is None
    table.add_widget(text_widget, col=1, row=2)
    assert table.get_widget(col=1, row=2) == text_widget
    table.remove_widget(col=1, row=2)
    assert table.get_widget(col=1, row=2) is None


def test_add_row():
    table = CanvasTable(label='table1', pos_x=50, pos_y=300, column_widths=[10], row_heights=[1, 2, 3])

    text_1 = CanvasText(text='text1', pos_x=200, pos_y=300)
    text_2 = CanvasText(text='text1', pos_x=200, pos_y=300)
    text_3 = CanvasText(text='text1', pos_x=200, pos_y=300)

    table.add_widget(text_1, col=1, row=1)
    table.add_widget(text_2, col=1, row=2)
    table.add_widget(text_3, col=1, row=3)

    assert table._row_heights[1] == 1
    assert table._row_heights[2] == 2
    assert table._row_heights[3] == 3

    table.add_row(row=2, height=10)

    assert table._row_heights[1] == 1
    assert table._row_heights[2] == 10
    assert table._row_heights[3] == 2
    assert table._row_heights[4] == 3

    assert table.get_widget(col=1, row=1) == text_1
    assert table.get_widget(col=1, row=2) is None
    assert table.get_widget(col=1, row=3) == text_2
    assert table.get_widget(col=1, row=4) == text_3

def test_remove_row():
    table = CanvasTable(label='table1', pos_x=50, pos_y=300, column_widths=[10], row_heights=[1, 2, 3, 10])

    text_1 = CanvasText(text='text1', pos_x=200, pos_y=300)
    text_2 = CanvasText(text='text1', pos_x=200, pos_y=300)
    text_3 = CanvasText(text='text1', pos_x=200, pos_y=300)

    table.add_widget(text_1, col=1, row=1)
    table.add_widget(text_2, col=1, row=2)
    table.add_widget(text_3, col=1, row=4)

    assert table._row_heights[1] == 1
    assert table._row_heights[2] == 2
    assert table._row_heights[3] == 3
    assert table._row_heights[4] == 10

    assert table.get_widget(col=1, row=1) == text_1
    assert table.get_widget(col=1, row=2) == text_2
    assert table.get_widget(col=1, row=3) is None
    assert table.get_widget(col=1, row=4) == text_3

    table.remove_row(row=2)

    assert table._row_heights[1] == 1
    assert table._row_heights[2] == 3
    assert table._row_heights[3] == 10

    assert table.get_widget(col=1, row=1) == text_1
    assert table.get_widget(col=1, row=2) is None
    assert table.get_widget(col=1, row=3) == text_3


def test_set_row_height():
    table = CanvasTable(label='table1', pos_x=50, pos_y=300, column_widths=[10], row_heights=[1, 2, 3, 10])

    assert table._row_heights[2] == 2

    table.set_row_height(25, row=2)

    assert table._row_heights[2] == 25


def test_add_column():
    table = CanvasTable(label='table1', pos_x=50, pos_y=300, column_widths=[5, 20, 10], row_heights=[1])

    text_1 = CanvasText(text='text1', pos_x=200, pos_y=300)
    text_2 = CanvasText(text='text1', pos_x=200, pos_y=300)
    text_3 = CanvasText(text='text1', pos_x=200, pos_y=300)

    table.add_widget(text_1, col=1, row=1)
    table.add_widget(text_2, col=2, row=1)
    table.add_widget(text_3, col=3, row=1)

    assert table._column_widths[1] == 5
    assert table._column_widths[2] == 20
    assert table._column_widths[3] == 10

    table.add_column(col=3, width=350)

    assert table._column_widths[1] == 5
    assert table._column_widths[2] == 20
    assert table._column_widths[3] == 350
    assert table._column_widths[4] == 10

    assert table.get_widget(col=1, row=1) == text_1
    assert table.get_widget(col=2, row=1) == text_2
    assert table.get_widget(col=3, row=1) is None
    assert table.get_widget(col=4, row=1) == text_3


def test_remove_column():
    table = CanvasTable(label='table1', pos_x=50, pos_y=300, column_widths=[5, 20, 7, 10], row_heights=[1, 5])

    text_1 = CanvasText(text='text1', pos_x=200, pos_y=300)
    text_2 = CanvasText(text='text1', pos_x=200, pos_y=300)
    text_3 = CanvasText(text='text1', pos_x=200, pos_y=300)

    table.add_widget(text_1, col=1, row=2)
    table.add_widget(text_2, col=3, row=2)
    table.add_widget(text_3, col=4, row=2)

    assert table._column_widths[1] == 5
    assert table._column_widths[2] == 20
    assert table._column_widths[3] == 7
    assert table._column_widths[4] == 10

    assert table.get_widget(col=1, row=2) == text_1
    assert table.get_widget(col=2, row=2) is None
    assert table.get_widget(col=3, row=2) == text_2
    assert table.get_widget(col=4, row=2) == text_3

    table.remove_column(col=3)

    assert table._column_widths[1] == 5
    assert table._column_widths[2] == 20
    assert table._column_widths[3] == 10

    assert table.get_widget(col=1, row=2) == text_1
    assert table.get_widget(col=2, row=2) is None
    assert table.get_widget(col=3, row=2) == text_3



'''



def test_widget_to_dict():
    assert False

def test_set_column_width():
    assert False

def test_add_widget_calc_position():
    assert False

def test_me_good():
    assert False
    # TODO
    # ADD IMGLOADER TESTS FOR THIS CLASS
'''
