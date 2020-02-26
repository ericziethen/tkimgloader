
import pytest

from imgloader import ConfigDrawer


def test_button_dic_initialized():
    drawer = ConfigDrawer('fake_canvas')

    assert 'image_buttons' in drawer.config
    assert not drawer.config['image_buttons']


def test_add_button():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=False, images=['path1', 'path2', 'path3'], redraw=False)

    assert 'butt1' in drawer.config['image_buttons']
    assert drawer.config['image_buttons']['butt1']['x'] == 100
    assert drawer.config['image_buttons']['butt1']['y'] == 200
    assert not drawer.config['image_buttons']['butt1']['orig_image_on_release']
    assert drawer.config['image_buttons']['butt1']['images']['1'] == 'path1'
    assert drawer.config['image_buttons']['butt1']['images']['2'] == 'path2'
    assert drawer.config['image_buttons']['butt1']['images']['3'] == 'path3'
    assert drawer.config['image_buttons']['butt1']['current_image'] == 1
    assert 'butt1' in drawer.canvas_image_button_details
    assert 'on_release_callback' in drawer.canvas_image_button_details['butt1']
    assert not drawer.canvas_image_button_details['butt1']['on_release_callback']


def test_image_button_id_available():
    drawer = ConfigDrawer('fake_canvas')

    assert drawer.image_button_id_available('butt1')
    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=False, images=['path1', 'path2', 'path3'], redraw=False)
    assert not drawer.image_button_id_available('butt1')


def test_add_button_orig_image_on_release():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1', 'path2', 'path3'], redraw=False)

    assert drawer.config['image_buttons']['butt1']['orig_image_on_release']


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


def test_adjust_button_position():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1', 'path2', 'path3'], redraw=False)
    assert drawer.config['image_buttons']['butt1']['x'] == 100
    assert drawer.config['image_buttons']['butt1']['y'] == 200

    drawer._update_image_position(button_id='butt1', pos_x=400, pos_y=600, redraw=False)
    assert drawer.config['image_buttons']['butt1']['x'] == 400
    assert drawer.config['image_buttons']['butt1']['y'] == 600


def test_move_button_relative():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1', 'path2', 'path3'], redraw=False)
    assert drawer.config['image_buttons']['butt1']['x'] == 100
    assert drawer.config['image_buttons']['butt1']['y'] == 200

    drawer.move_image_button(button_id='butt1', move_x=150, move_y=-75, redraw=False)
    assert drawer.config['image_buttons']['butt1']['x'] == 250
    assert drawer.config['image_buttons']['butt1']['y'] == 125


def test_show_next_image():
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


def test_show_previous_image():
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


def test_show_next_previous_image_single_image():
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


def test_remove_current_image_reindex_list():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=False,
                            images=['path1', 'path2', 'path3', 'path4'], redraw=False)

    assert len(drawer.config['image_buttons']['butt1']['images']) == 4
    assert drawer.config['image_buttons']['butt1']['images']['1'] == 'path1'
    assert drawer.config['image_buttons']['butt1']['images']['2'] == 'path2'
    assert drawer.config['image_buttons']['butt1']['images']['3'] == 'path3'
    assert drawer.config['image_buttons']['butt1']['images']['4'] == 'path4'
    assert drawer.config['image_buttons']['butt1']['current_image'] == 1

    drawer.remove_current_button_image(button_id='butt1', redraw=False)
    assert len(drawer.config['image_buttons']['butt1']['images']) == 3
    assert drawer.config['image_buttons']['butt1']['images']['1'] == 'path2'
    assert drawer.config['image_buttons']['butt1']['images']['2'] == 'path3'
    assert drawer.config['image_buttons']['butt1']['images']['3'] == 'path4'
    assert drawer.config['image_buttons']['butt1']['current_image'] == 3


def test_remove_last_image_delete_button():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1'], redraw=False)
    assert 'butt1' in drawer.config['image_buttons']

    drawer.remove_current_button_image(button_id='butt1', redraw=False)
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
