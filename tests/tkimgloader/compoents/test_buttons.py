
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


def test_add_button_orig_image_on_release():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1', 'path2', 'path3'], redraw=False)

    assert drawer.config['image_buttons']['butt1']['orig_image_on_release']


def test_reject_duplicate_ids():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1', 'path2', 'path3'], redraw=False)

    with pytest.raises(ValueError):
        drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1', 'path2', 'path3'], redraw=False)


def test_adjust_button_position():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1', 'path2', 'path3'], redraw=False)
    assert drawer.config['image_buttons']['butt1']['x'] == 100
    assert drawer.config['image_buttons']['butt1']['y'] == 200

    drawer.update_image_position(button_id='butt1', pos_x=400, pos_y=600, redraw=False)
    assert drawer.config['image_buttons']['butt1']['x'] == 400
    assert drawer.config['image_buttons']['butt1']['y'] == 600


'''
def test_move_button_relative():
    drawer = ConfigDrawer('fake_canvas')

    drawer.add_image_button(button_id='butt1', pos_x=100, pos_y=200, orig_on_release=True, images=['path1', 'path2', 'path3'], redraw=False)
    assert drawer.config['image_buttons']['butt1']['x'] == 100
    assert drawer.config['image_buttons']['butt1']['y'] == 200

    drawer.move_image_button(button_id='butt1', move_x=400, move_y=-50, redraw=False)
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


