
from tkimgloader.widgets import CanvasText, WidgetType


def test_create_widget():
    widget = CanvasText(text='myText', pos_x=200, pos_y=300)

    assert widget.widget_type == WidgetType.TEXT
    assert widget.pos_x == 200
    assert widget.pos_y == 300
    assert widget.text == 'myText'


def test_widget_str():
    widget = CanvasText(text='myText', pos_x=200, pos_y=300)

    assert str(widget) == 'myText (Text) [200,300]'


def test_widget_to_dict():
    widget = CanvasText(text='myText', pos_x=200, pos_y=300)

    assert widget.to_dict() == {
        'label': None,
        'x': 200,
        'y': 300,
        'text': 'myText'
    }


def test_move_to():
    widget = CanvasText(text='myText', pos_x=200, pos_y=300)
    assert widget.pos_x == 200
    assert widget.pos_y == 300

    widget.move_to(pos_x=800, pos_y=600)
    assert widget.pos_x == 800
    assert widget.pos_y == 600


def test_move_by():
    widget = CanvasText(text='myText', pos_x=200, pos_y=300)
    assert widget.pos_x == 200
    assert widget.pos_y == 300

    widget.move_by(move_x=-50, move_y=150)
    assert widget.pos_x == 150
    assert widget.pos_y == 450
