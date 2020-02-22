
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

    drawer.update_image_position(button_id='butt1', pos_x=400, pos_y=600, redraw=False)
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

    drawer.remove_image_button(button_id='butt1', redraw=False)
    assert 'butt1' not in drawer.config['image_buttons']


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





'''
def test_remove_last_image_delete_button():

def test_remove_middle_image():


def test_remove_last_image():

def test_remove_current_image():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True,
                            images=['path1', 'path2', 'path3', 'path4', 'path5'], redraw=False)

    assert len(drawer.config['image_buttons']['butt1']['images']) == 4
    assert drawer.config['image_buttons']['butt1']['current_image'] == 1

    # Remove First Image
    drawer.remove_current_button_image(button_id='butt1', redraw=False)
    assert len(drawer.config['image_buttons']['butt1']['images']) == 4
    assert drawer.config['image_buttons']['butt1']['current_image'] == 4

    # Remove Last Image


    # Remove Middle Image


    drawer.next_button_image(button_id='butt1', redraw=False)
    drawer.next_button_image(button_id='butt1', redraw=False)
    assert drawer.config['image_buttons']['butt1']['current_image'] == 3

    drawer.remove_current_button_image(button_id='butt1', redraw=False)
    assert len(drawer.config['image_buttons']['butt1']['images']) == 3
    assert drawer.config['image_buttons']['butt1']['current_image'] == 2
'''



'''




def test_remove_current_image():
    assert False


def test_remove_button():
    assert False
'''

'''

Current config is something like
    {
        "background": "AufstellungsScreen\\grafik_cpr-0000001450_Background.jpg",
        "text": {
            "Pos": {
                "x": 100,
                "y": 100,
                "text": "Pos"
            }
        }
    }

Roles for Button/Switches
    - Config:
        - id, position for the image button
        - images to be used as confirm buttons i.e. change back on release
        - images to be used as switch, i.e. stay the same

    - Imgloader:
        - keep track of callbacks for each button based on id (unique, cant add 2) to be used on release
        - update graphics on click
        - update grahics on release (and call callback)
        - keep track of the current images for each button

    - Using Program:
        - after button initialized, set the callbacks for each buttons
            - Params TBC
        - Left Mouse - Next Image
        - Right Mouse - Previoue Image

Expected Config:

    "image_buttons": {
        "{id}": {
                "x": 100,
                "y": 100,
                "orig_image_on_release: True,   # Return to the original image on release
                "images": {
                    "1": "path1",                  # This will be the original image
                    "2": "path2",
                }

        }
        "{id}": {

        }
    }




'''


