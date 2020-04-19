from tkimgloader.widgets import (
    CanvasTable, WidgetType
)


def test_create_widget():
    widget = CanvasTable(
        label='table1', pos_x=100, pos_y=200,
        column_widths=(50, 100, 100),
        row_heights=(100, 200)
    )

    assert widget.label == 'table1'
    assert widget.widget_type == WidgetType.TABLE
    assert widget.pos_x == 100
    assert widget.pos_y == 200

    assert len(widget.column_widths) == 3
    assert len(widget.row_heights) == 2

    assert widget.column_widths[1] == 50
    assert widget.column_widths[2] == 100
    assert widget.column_widths[3] == 100

    assert widget.row_heights[1] == 100
    assert widget.row_heights[2] == 200


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







'''

def test_add_widget():
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
