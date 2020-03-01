
import copy
import functools
import json
import logging

import tkinter as tk

from PIL import ImageTk

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name







class ConfigDrawer():  # pylint: disable=too-many-public-methods
    def __init__(self, canvas):
        self.canvas = canvas
        self.background_path = ''
        self.widgets = {}





        # OLD - REMOVE WHEN REFACTORED
        self.config = {'background': None, 'text': {}, 'image_buttons': {}} # TODO - To be replaced, generate config from Widgets
        self.saved_img_config = copy.deepcopy(self.config)


        self.images = {}
        self.canvas_image_button_details = {}
        self.canvas_text_details = {}
        self.config_path = None

    @property
    def unsaved_changes(self):
        # TODO - Call cal config function and compare that !!!
        return self.config != self.saved_img_config

    def __eq__(self, other):
        # Compare config
        if self.config != other.config:
            print('##### Config Differs')
            print(self.config)
            print(other.config)
            return False

        # compare comfig path
        if self.config_path != other.config_path:
            print('##### Config Path Differs')
            print(self.config_path)
            print(other.config_path)
            return False

        # compare image keys
        if self.images.keys() != other.images.keys():
            print('##### Image Keys Differs')
            print(self.images.keys())
            print(other.images.keys())
            return False

        # compare canvas_image_button_details keys
        if self.canvas_image_button_details.keys() != other.canvas_image_button_details.keys():
            print('##### Image Button Keys Differs')
            print(self.canvas_image_button_details.keys())
            print(other.canvas_image_button_details.keys())
            return False

        return True

    def _add_widget(self, widget):
        widget_id = _form_full_widget_id(widget.id, widget.widget_type)

        if widget_id in self.widgets:
            raise ValueError(F'Widget type "{widget.widget_type}" with Id "{widget.id}" already exists"')

        self.widgets[widget_id] = widget

    def contains_widget(self, widget_id, widget_type):
        return _form_full_widget_id(widget_id, widget_type) in self.widgets





























    def load_background(self, path, redraw=True):
        self.background_path = path

        if redraw:
            logger.debug(F'Drawing Background file "{path}"')

            background = ImageTk.PhotoImage(file=path)
            self.images['background'] = background  # Make the image persistent

            self.canvas.config(width=background.width(), height=background.height())
            self.canvas.create_image(0, 0, image=background, anchor=tk.NW)

    def _load_config(self, config, *, config_path, redraw=True):
        # Set config vars
        self.config_path = config_path

        # Load the background
        if 'background' in config:
            self.load_background(config['background'], redraw=redraw)

        # Load the Text Items
        if 'text' in config:
            for text_id, text_item in config['text'].items():
                self.add_text(text_id=text_id, text=text_item['text'],
                              pos_x=text_item['x'], pos_y=text_item['y'], redraw=redraw)

        # Load the image button items
        if 'image_buttons' in config:
            for button_id, button_dic in config['image_buttons'].items():
                self.add_image_button(button_id=button_id, pos_x=button_dic['x'], pos_y=button_dic['y'],
                                      orig_on_release=button_dic['orig_image_on_release'],
                                      current_image=button_dic['current_image'],
                                      images=list(button_dic['images'].values()), redraw=redraw)

        self.saved_img_config = copy.deepcopy(self.config)

    def load_config_file(self, config_path, *, redraw=True):
        config = load_json(config_path)
        logger.debug(F'Load Config: {config}')
        self._load_config(config, config_path=config_path, redraw=redraw)

    def save_config_to_file(self, config_path):
        dump_json(config_path, self.config)
        self.config_path = config_path
        self.saved_img_config = copy.deepcopy(self.config)

    # Text Related Functionality
    def add_text(self, *, text_id, text, pos_x, pos_y, redraw=True):
        text_dict = {'text': text, 'x': pos_x, 'y': pos_y}
        self.config['text'][text_id] = text_dict
        self.canvas_text_details[text_id] = {}

        if redraw:
            logger.debug(F'''Create Text "{text_dict['text']}" @ {text_dict['x']}x{text_dict['y']}''')
            widget = self.canvas.create_text(
                text_dict['x'], text_dict['y'], anchor=tk.NW,
                font="Times 10 italic bold", text=text_dict['text'])
            self.canvas_text_details[text_id]['widget'] = widget

    def _update_text_position(self, *, text_id, pos_x, pos_y, redraw=True):
        self.config['text'][text_id]['x'] = pos_x
        self.config['text'][text_id]['y'] = pos_y
        if redraw:
            self.canvas.coords(self.canvas_text_details[text_id]['widget'], pos_x, pos_y)

    def move_text(self, *, text_id, move_x, move_y, redraw=True):
        self._update_text_position(
            text_id=text_id,
            pos_x=self.config['text'][text_id]['x'] + move_x,
            pos_y=self.config['text'][text_id]['y'] + move_y,
            redraw=redraw)

    def remove_text(self, *, text_id, redraw=True):
        if redraw:
            self.canvas.delete(self.canvas_text_details[text_id]['widget'])
        del self.canvas_text_details[text_id]
        del self.config['text'][text_id]

    # Image Button Related Functionality
    def image_button_id_available(self, button_id):
        return button_id not in self.config['image_buttons']

    def add_image_button(self, *, button_id, pos_x, pos_y, orig_on_release, images, current_image=1, redraw=True):
        if button_id in self.config['image_buttons']:
            raise ValueError('No Duplicate IDs for Buttons allowed')

        if not images:
            raise ValueError('Image list cannot be empty')

        self.canvas_image_button_details[button_id] = {'on_release_callback': None}

        image_dic = {str(idx): path for idx, path in enumerate(images, 1)}

        button_dic = {
            'x': pos_x,
            'y': pos_y,
            'orig_image_on_release': orig_on_release,
            'current_image': current_image,
            'images': image_dic
        }

        self.config['image_buttons'][button_id] = button_dic
        if redraw:
            # Setup all images
            for img_path in button_dic['images'].values():
                if img_path not in self.images:
                    self.images[img_path] = ImageTk.PhotoImage(file=img_path)

            current_img_path = button_dic['images'][str(button_dic['current_image'])]
            current_img = self.images[current_img_path]

            img_button = self.canvas.create_image(button_dic['x'], button_dic['y'], image=current_img)
            self.canvas.tag_bind(img_button, '<Button-1>',
                                 functools.partial(self.image_button_pressed, button_id=button_id))
            self.canvas.tag_bind(img_button, '<ButtonRelease-1>',
                                 functools.partial(self.image_button_released, button_id=button_id))

            self.canvas.tag_bind(img_button, '<Button-3>',
                                 functools.partial(self.image_button_pressed, button_id=button_id))
            self.canvas.tag_bind(img_button, '<ButtonRelease-3>',
                                 functools.partial(self.image_button_released, button_id=button_id))

            self.canvas_image_button_details[button_id]['widget'] = img_button

    def add_image_button_callback(self, *, button_id, func):
        self.canvas_image_button_details[button_id]['on_release_callback'] = func

    def _update_image_position(self, *, button_id, pos_x, pos_y, redraw=True):
        self.config['image_buttons'][button_id]['x'] = pos_x
        self.config['image_buttons'][button_id]['y'] = pos_y
        if redraw:
            self.canvas.coords(self.canvas_image_button_details[button_id]['widget'], pos_x, pos_y)

    def move_image_button(self, *, button_id, move_x, move_y, redraw=True):
        self._update_image_position(
            button_id=button_id,
            pos_x=self.config['image_buttons'][button_id]['x'] + move_x,
            pos_y=self.config['image_buttons'][button_id]['y'] + move_y,
            redraw=redraw)

    def next_button_image(self, *, button_id, redraw=True):
        button = self.config['image_buttons'][button_id]
        previous_image = button['current_image']
        if len(button['images']) > button['current_image']:
            button['current_image'] += 1
        else:
            button['current_image'] = 1

        if redraw and (previous_image != button['current_image']):
            img_path = button['images'][str(button['current_image'])]
            self.canvas.itemconfig(
                self.canvas_image_button_details[button_id]['widget'],
                image=self.images[img_path])

    def previous_button_image(self, *, button_id, redraw=True):
        button = self.config['image_buttons'][button_id]
        previous_image = button['current_image']
        if button['current_image'] > 1:
            button['current_image'] -= 1
        else:
            button['current_image'] = len(button['images'])

        if redraw and (previous_image != button['current_image']):
            img_path = button['images'][str(button['current_image'])]
            self.canvas.itemconfig(
                self.canvas_image_button_details[button_id]['widget'],
                image=self.images[img_path])

    def add_new_button_image(self, *, button_id, path_list, redraw=True):
        # The lazy Way, Delete Old Button and Create a new One
        old_button = copy.deepcopy(self.config['image_buttons'][button_id])

        # Add Image to Path
        new_path_list = list(old_button['images'].values())
        new_path_list = (new_path_list[:old_button['current_image']] +
                         path_list + new_path_list[old_button['current_image']:])

        # Remove Old Button
        self.remove_image_button(button_id=button_id, redraw=redraw)

        # Add new Button
        self.add_image_button(
            button_id=button_id, pos_x=old_button['x'], pos_y=old_button['y'],
            orig_on_release=old_button['orig_image_on_release'],
            current_image=old_button['current_image'] + 1,
            images=list(new_path_list), redraw=redraw)

    def remove_current_button_image(self, *, button_id, redraw=True):
        # Delete this buttn if its the only image that is deleted
        if len(self.config['image_buttons'][button_id]['images']) == 1:
            self.remove_image_button(button_id=button_id, redraw=redraw)
            return True

        # Remove the button
        button = self.config['image_buttons'][button_id]

        image_to_delete = button['current_image']

        # Set the previous image as the current one
        self.previous_button_image(button_id=button_id, redraw=redraw)

        # Remove the Image
        del button['images'][str(image_to_delete)]

        # Reindex the remaining images
        image_dic = {str(idx): path for idx, path in enumerate(button['images'].values(), 1)}
        button['images'] = image_dic

        # Set the new Current Image
        if image_to_delete > 1:
            button['current_image'] = image_to_delete - 1
        else:
            button['current_image'] = len(button['images'])
        return False

    def remove_image_button(self, *, button_id, redraw=True):
        if redraw:
            self.canvas.delete(self.canvas_image_button_details[button_id]['widget'])
        del self.canvas_image_button_details[button_id]
        del self.config['image_buttons'][button_id]

    def image_button_pressed(self, event, *, button_id):
        print(F'### image_button_pressed({button_id}) ###')
        print('event.num', event.num)
        print('orig_image_on_release', self.config['image_buttons'][button_id]['orig_image_on_release'])
        if (event.num == 1) and (self.config['image_buttons'][button_id]['orig_image_on_release']):
            self.next_button_image(button_id=button_id)

    def image_button_released(self, event, *, button_id):
        if event.num == 1:
            if self.config['image_buttons'][button_id]['orig_image_on_release']:
                self.previous_button_image(button_id=button_id)
            else:
                self.next_button_image(button_id=button_id)
        elif (event.num == 3) and not self.config['image_buttons'][button_id]['orig_image_on_release']:
            self.previous_button_image(button_id=button_id)

        callback = self.canvas_image_button_details[button_id]['on_release_callback']
        if callback:
            callback()


def _form_full_widget_id(widget_id, widget_type):
    return widget_type.value + '_' + widget_id


def load_json(file_path):
    with open(file_path) as file_ptr:
        return json.load(file_ptr)


def dump_json(file_path, config):
    with open(file_path, 'w') as file_ptr:
        json.dump(config, file_ptr, indent=4)
