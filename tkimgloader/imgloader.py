
import copy
import functools
import json
import logging

import tkinter as tk

from PIL import ImageTk

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ConfigDrawer():
    def __init__(self, canvas):
        self.canvas = canvas
        self.config = {'background': None, 'text': {}, 'image_buttons': {}}
        self.saved_img_config = copy.deepcopy(self.config)
        self.images = {}
        self.canvas_image_button_details = {}
        self.config_path = None

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

    @property
    def background(self):
        return self.config['background']

    @property
    def dimensions(self):
        if self.config['background']:
            return (self.images['background'].width(), self.images['background'].height())
        return (0, 0)

    @property
    def unsaved_changes(self):
        return self.config != self.saved_img_config

    def load_background(self, path, redraw=True):
        self.config['background'] = path
        if redraw:
            self.draw()

    def draw(self):
        logger.debug(F'Drawing Content: {self.config}')

        # Draw the Background
        if self.config['background']:
            img_path = self.config['background']
            logger.debug(F'Drawing Background file "{img_path}"')

            background = ImageTk.PhotoImage(file=img_path)
            self.images['background'] = background  # Make the image persistent

            self.canvas.config(width=background.width(), height=background.height())
            self.canvas.create_image(0, 0, image=background, anchor=tk.NW)
        else:
            logger.debug('No Background to Draw')

        # Draw Text
        if 'text' in self.config and self.config['text']:
            for _, text_dict in self.config['text'].items():
                logger.debug(F'''Create Text "{text_dict['text']}" @ {text_dict['x']}x{text_dict['y']}''')
                self.canvas.create_text(
                    text_dict['x'], text_dict['y'], anchor=tk.NW,
                    font="Times 10 italic bold", text=text_dict['text'])

        for button_id, button_dic in self.config['image_buttons'].items():
            img_path = button_dic['images'][str(button_dic['current_image'])]
            if img_path in self.images:
                image = self.images[img_path]
            else:
                image = ImageTk.PhotoImage(file=img_path)
                self.images[img_path] = image

                print(F'Button: "{button_id}" - Current Image: "{button_dic["current_image"]}"')

            img_button = self.canvas.create_image(button_dic['x'], button_dic['y'], image=image)
            self.canvas.tag_bind(img_button, '<Button-1>',
                                 functools.partial(self.image_button_pressed, button_id=button_id))
            self.canvas.tag_bind(img_button, '<ButtonRelease-1>',
                                 functools.partial(self.image_button_released, button_id=button_id))

            self.canvas.tag_bind(img_button, '<Button-3>',
                                 functools.partial(self.image_button_pressed, button_id=button_id))
            self.canvas.tag_bind(img_button, '<ButtonRelease-3>',
                                 functools.partial(self.image_button_released, button_id=button_id))

            self.canvas_image_button_details[button_id]['canvas_id'] = img_button

        # print('Canvas Items:', self.canvas.find_all())
        # print('Canvas Item Count:', len(self.canvas.find_all()))

    def _load_config(self, config, *, config_path, redraw=True):
        # Set config vars
        self.config_path = config_path

        # Load the background
        if 'background' in config:
            self.load_background(config['background'], redraw=False)

        # Load the Text Items
        if 'text' in config:
            for text_id, text_item in config['text'].items():
                self.add_text(text_id=text_id, text=text_item['text'],
                              pos_x=text_item['x'], pos_y=text_item['y'], redraw=False)

        # Load the image button items
        if 'image_buttons' in config:
            for button_id, button_dic in config['image_buttons'].items():
                self.add_image_button(button_id=button_id, pos_x=button_dic['x'], pos_y=button_dic['y'],
                                      orig_on_release=button_dic['orig_image_on_release'],
                                      current_image=button_dic['current_image'],
                                      images=list(button_dic['images'].values()), redraw=False)

        self.saved_img_config = copy.deepcopy(self.config)

        # Redraw
        if redraw:
            self.draw()

    def load_config_file(self, config_path, *, redraw=True):
        config = load_json(config_path)
        self._load_config(config, config_path=config_path, redraw=redraw)

    def save_config_to_file(self, config_path):
        dump_json(config_path, self.config)
        self.config_path = config_path
        self.saved_img_config = copy.deepcopy(self.config)

    # Text Related Functionality
    def add_text(self, *, text_id, text, pos_x, pos_y, redraw=True):
        self.config['text'][text_id] = {'text': text, 'x': pos_x, 'y': pos_y}
        if redraw:
            self.draw()

    def update_text_position(self, *, text_id, pos_x, pos_y, redraw=True):
        self.config['text'][text_id]['x'] = pos_x
        self.config['text'][text_id]['y'] = pos_y
        if redraw:
            self.draw()

    def move_text(self, *, text_id, move_x, move_y, redraw=True):
        self.update_text_position(
            text_id=text_id,
            pos_x=self.config['text'][text_id]['x'] + move_x,
            pos_y=self.config['text'][text_id]['y'] + move_y,
            redraw=redraw)

    def remove_text(self, *, text_id, redraw=True):
        del self.config['text'][text_id]
        if redraw:
            self.draw()

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
            self.draw()

    def add_image_button_callback(self, *, button_id, func):
        self.canvas_image_button_details[button_id]['on_release_callback'] = func

    def update_image_position(self, *, button_id, pos_x, pos_y, redraw=True):
        self.config['image_buttons'][button_id]['x'] = pos_x
        self.config['image_buttons'][button_id]['y'] = pos_y
        if redraw:
            self.draw()

    def move_image_button(self, *, button_id, move_x, move_y, redraw=True):
        self.update_image_position(
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
            self.draw()

    def previous_button_image(self, *, button_id, redraw=True):
        button = self.config['image_buttons'][button_id]
        previous_image = button['current_image']
        if button['current_image'] > 1:
            button['current_image'] -= 1
        else:
            button['current_image'] = len(button['images'])

        if redraw and (previous_image != button['current_image']):
            self.draw()

    def remove_current_button_image(self, *, button_id, redraw=True):
        # Delete this buttn if its the only image that is deleted
        if len(self.config['image_buttons'][button_id]['images']) == 1:
            self.remove_image_button(button_id=button_id, redraw=redraw)
        else:
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

            if redraw:
                self.draw()

    def remove_image_button(self, *, button_id, redraw=True):
        del self.config['image_buttons'][button_id]
        del self.canvas_image_button_details[button_id]

        if redraw:
            self.draw()

    def image_button_pressed(self, event, *, button_id):
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


def load_json(file_path):
    with open(file_path) as file_ptr:
        return json.load(file_ptr)


def dump_json(file_path, config):
    with open(file_path, 'w') as file_ptr:
        json.dump(config, file_ptr, indent=4)
