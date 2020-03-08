
import pytest

from tkimgloader.imgloader import ConfigDrawer
from tkimgloader.widgets import ButtonType, WidgetType

'''

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!! DEFINE NEW TESTS BASED ON CODE



def test_add_button_type_switch():
    drawer = ConfigDrawer('fake_canvas')
    assert not drawer.widgets

    widget = drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=False,
                                     images=['path1', 'path2', 'path3'], current_image=2, redraw=False)

    assert drawer.contains_widget('butt1', WidgetType.BUTTON)
    assert widget.button_type == ButtonType.SWITCH
    assert widget.image_list == ['path1', 'path2', 'path3']
    assert widget.current_image == 2


def test_add_button_type_release():
    drawer = ConfigDrawer('fake_canvas')

    widget = drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True,
                                     images=['path1', 'path2', 'path3'], current_image=2, redraw=False)
    assert widget.button_type == ButtonType.RELEASE


def test_add_widget_duplicate_id():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=False, images=['path1', 'path2', 'path3'], redraw=False)

    with pytest.raises(ValueError):
        drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=False, images=['path1', 'path2', 'path3'], redraw=False)


def test_add_button_reject_empty_image_list():
    drawer = ConfigDrawer('fake_canvas')

    with pytest.raises(ValueError):
        drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=[], redraw=False)


def test_reject_duplicate_ids():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1', 'path2', 'path3'], redraw=False)

    with pytest.raises(ValueError):
        drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1', 'path2', 'path3'], redraw=False)

    drawer.add_image_button(button_id='butt2', pos_x=100, pos_y=200, orig_on_release=True, images=['path1', 'path2', 'path3'], redraw=False)





########################
##### UNREFACTORED #####
########################


# TODO - Once Classes are implemented
# def test_duplicate_widget_ids():







### TODO !!! SOME TESTS NEED TO BE MOVED INTO THE WIDGET, i.e. the NEXT IMAGE STUFF






def test_show_next_image():  # TODO - Move to Widget Test
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True,
                            images=['path1', 'path2', 'path3', 'path2'], redraw=False)

    assert len(drawer.config['image_buttons']['butt1']['images']) == 4
    assert drawer.config['image_buttons']['butt1']['current_image'] == 1

    drawer.next_button_image(button_id='butt1', redraw=False)
    assert drawer.config['image_buttons']['butt1']['current_image'] == 2

    drawer.next_button_image(button_id='butt1', redraw=False)
    assert drawer.config['image_buttons']['butt1']['current_image'] == 3

    drawer.next_button_image(button_id='butt1', redraw=False)
    assert drawer.config['image_buttons']['butt1']['current_image'] == 4

    drawer.next_button_image(button_id='butt1', redraw=False)
    assert drawer.config['image_buttons']['butt1']['current_image'] == 1


def test_show_previous_image():  # TODO - Move to Widget Test
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True,
                            images=['path1', 'path2', 'path3', 'path2'], redraw=False)

    assert len(drawer.config['image_buttons']['butt1']['images']) == 4
    assert drawer.config['image_buttons']['butt1']['current_image'] == 1

    drawer.previous_button_image(button_id='butt1', redraw=False)
    assert drawer.config['image_buttons']['butt1']['current_image'] == 4

    drawer.previous_button_image(button_id='butt1', redraw=False)
    assert drawer.config['image_buttons']['butt1']['current_image'] == 3

    drawer.previous_button_image(button_id='butt1', redraw=False)
    assert drawer.config['image_buttons']['butt1']['current_image'] == 2

    drawer.previous_button_image(button_id='butt1', redraw=False)
    assert drawer.config['image_buttons']['butt1']['current_image'] == 1


def test_show_next_previous_image_single_image():  # TODO - Move to Widget Test
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1'], redraw=False)

    assert len(drawer.config['image_buttons']['butt1']['images']) == 1
    assert drawer.config['image_buttons']['butt1']['current_image'] == 1

    drawer.next_button_image(button_id='butt1', redraw=False)
    assert drawer.config['image_buttons']['butt1']['current_image'] == 1

    drawer.previous_button_image(button_id='butt1', redraw=False)
    assert drawer.config['image_buttons']['butt1']['current_image'] == 1


def test_remove_button():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1'], redraw=False)
    assert 'butt1' in drawer.config['image_buttons']
    assert 'butt1' in drawer.canvas_image_button_details

    drawer.remove_image_button(button_id='butt1', redraw=False)
    assert 'butt1' not in drawer.config['image_buttons']
    assert 'butt1' not in drawer.canvas_image_button_details


def test_add_new_button_image_middle_position():  # TODO - Move to Widget Test
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=False,
                            images=['path1', 'path3'], redraw=False)
    assert len(drawer.config['image_buttons']['butt1']['images']) == 2
    assert drawer.config['image_buttons']['butt1']['images']['1'] == 'path1'
    assert drawer.config['image_buttons']['butt1']['images']['2'] == 'path3'
    assert drawer.config['image_buttons']['butt1']['current_image'] == 1

    drawer.add_new_button_image(button_id='butt1', path_list=['path2'], redraw=False)

    assert len(drawer.config['image_buttons']['butt1']['images']) == 3
    assert drawer.config['image_buttons']['butt1']['images']['1'] == 'path1'
    assert drawer.config['image_buttons']['butt1']['images']['2'] == 'path2'
    assert drawer.config['image_buttons']['butt1']['images']['3'] == 'path3'
    assert drawer.config['image_buttons']['butt1']['current_image'] == 2


def test_add_multiple_new_button_image_middle_position():  # TODO - Move to Widget Test
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=False,
                            images=['path1', 'path4'], redraw=False)
    assert len(drawer.config['image_buttons']['butt1']['images']) == 2
    assert drawer.config['image_buttons']['butt1']['images']['1'] == 'path1'
    assert drawer.config['image_buttons']['butt1']['images']['2'] == 'path4'
    assert drawer.config['image_buttons']['butt1']['current_image'] == 1

    drawer.add_new_button_image(button_id='butt1', path_list=['path2','path3'], redraw=False)

    assert len(drawer.config['image_buttons']['butt1']['images']) == 4
    assert drawer.config['image_buttons']['butt1']['images']['1'] == 'path1'
    assert drawer.config['image_buttons']['butt1']['images']['2'] == 'path2'
    assert drawer.config['image_buttons']['butt1']['images']['3'] == 'path3'
    assert drawer.config['image_buttons']['butt1']['images']['4'] == 'path4'
    assert drawer.config['image_buttons']['butt1']['current_image'] == 2


def test_add_new_button_image_end_position():  # TODO - Move to Widget Test
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=False,
                            images=['path1', 'path2'], redraw=False)
    assert len(drawer.config['image_buttons']['butt1']['images']) == 2
    assert drawer.config['image_buttons']['butt1']['images']['1'] == 'path1'
    assert drawer.config['image_buttons']['butt1']['images']['2'] == 'path2'
    assert drawer.config['image_buttons']['butt1']['current_image'] == 1

    drawer.next_button_image(button_id='butt1', redraw=False)
    assert drawer.config['image_buttons']['butt1']['current_image'] == 2

    drawer.add_new_button_image(button_id='butt1', path_list=['path3'], redraw=False)

    assert len(drawer.config['image_buttons']['butt1']['images']) == 3
    assert drawer.config['image_buttons']['butt1']['images']['1'] == 'path1'
    assert drawer.config['image_buttons']['butt1']['images']['2'] == 'path2'
    assert drawer.config['image_buttons']['butt1']['images']['3'] == 'path3'
    assert drawer.config['image_buttons']['butt1']['current_image'] == 3


def test_remove_current_image_reindex_list():  # TODO - Move to Widget Test
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=False,
                            images=['path1', 'path2', 'path3', 'path4'], redraw=False)

    assert len(drawer.config['image_buttons']['butt1']['images']) == 4
    assert drawer.config['image_buttons']['butt1']['images']['1'] == 'path1'
    assert drawer.config['image_buttons']['butt1']['images']['2'] == 'path2'
    assert drawer.config['image_buttons']['butt1']['images']['3'] == 'path3'
    assert drawer.config['image_buttons']['butt1']['images']['4'] == 'path4'
    assert drawer.config['image_buttons']['butt1']['current_image'] == 1

    deleted = drawer.remove_current_button_image(button_id='butt1', redraw=False)
    assert not deleted
    assert len(drawer.config['image_buttons']['butt1']['images']) == 3
    assert drawer.config['image_buttons']['butt1']['images']['1'] == 'path2'
    assert drawer.config['image_buttons']['butt1']['images']['2'] == 'path3'
    assert drawer.config['image_buttons']['butt1']['images']['3'] == 'path4'
    assert drawer.config['image_buttons']['butt1']['current_image'] == 3


def test_remove_last_image_delete_button(): # TODO - f the removing is done in WIdget then how can we delete the button, otherwise don't allow deleting the last image
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1'], redraw=False)
    assert 'butt1' in drawer.config['image_buttons']

    deleted = drawer.remove_current_button_image(button_id='butt1', redraw=False)
    assert deleted
    assert 'butt1' not in drawer.config['image_buttons']

def test_equal_button():
    drawer1 = ConfigDrawer('fake_canvas')
    drawer2 = ConfigDrawer('fake_canvas')

    drawer1.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1'], redraw=False)
    drawer2.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1'], redraw=False)

    assert drawer1 == drawer2


def test_set_image_button_callback():
    def callback_func():
        pass

    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1'], redraw=False)
    assert not drawer.canvas_image_button_details['butt1']['on_release_callback']

    drawer.add_image_button_callback(button_id='butt1', func=callback_func)
    assert drawer.canvas_image_button_details['butt1']['on_release_callback'] == callback_func
'''