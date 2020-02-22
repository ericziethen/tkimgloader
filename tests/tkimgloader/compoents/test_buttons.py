
from imgloader import ConfigDrawer


#def test_add_button()















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

    "buttons": {
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


