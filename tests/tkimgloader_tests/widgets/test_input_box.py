

from tkimgloader.widgets import InputBox, WidgetType


def test_create_widget():
    widget = InputBox(pos_x=100, pos_y=200)

    assert widget.widget_type == WidgetType.INPUT_BOX
    assert widget.pos_x == 100
    assert widget.pos_y == 200


def test_widget_str():
    widget = InputBox(pos_x=100, pos_y=200)

    assert str(widget) == '(Input Box) [100,200]'

def test_widget_to_dict():
    widget = InputBox(pos_x=100, pos_y=200)

    assert widget.to_dict() == {
        'x': 100,
        'y': 200
    }

def test_move_to():
    widget = InputBox(pos_x=100, pos_y=200)
    assert widget.pos_x == 100
    assert widget.pos_y == 200

    widget.move_to(pos_x=800, pos_y=600)
    assert widget.pos_x == 800
    assert widget.pos_y == 600


def test_move_by():
    widget = InputBox(pos_x=200, pos_y=300)
    assert widget.pos_x == 200
    assert widget.pos_y == 300

    widget.move_by(move_x=-50, move_y=150)
    assert widget.pos_x == 150
    assert widget.pos_y == 450


def test_set_callback():
    def callback_func(text):
        pass

    widget = InputBox(pos_x=200, pos_y=300)

    assert not widget.input_confirm_callback
    widget.add_callback(input_confirm_callback=callback_func)
    assert widget.input_confirm_callback == callback_func
