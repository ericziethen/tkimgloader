
import copy
import functools
import json
import logging

import tkinter as tk

from PIL import ImageTk

from widgets import ButtonType, CanvasImageButton, CanvasText, WidgetType

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

    @property
    def dimensions(self):
        if 'background' in self.images:
            return (self.images['background'].width(), self.images['background'].height())
        return (0, 0)

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

    def _add_widget(self, widget, draw=True):
        widget_id = _form_full_widget_id(widget.id, widget.widget_type)

        if widget_id in self.widgets:
            raise ValueError(F'Widget type "{widget.widget_type}" with Id "{widget.id}" already exists"')

        self.widgets[widget_id] = widget
        if draw:
            widget.canvas = self.canvas
            self.widgets[widget_id].draw()

    def remove_widget(self, widget, draw=True):
        widget_id = _form_full_widget_id(widget.id, widget.widget_type)
        self.widgets[widget_id].destroy()
        del self.widgets[widget_id]

    def contains_widget(self, widget_id, widget_type):
        return _form_full_widget_id(widget_id, widget_type) in self.widgets

    def load_background(self, path, redraw=True):
        self.background_path = path

        if redraw:
            logger.debug(F'Drawing Background file "{path}"')

            background = ImageTk.PhotoImage(file=path)
            self.images['background'] = background

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
        text_widget = CanvasText(text_id=text_id, text=text, pos_x=pos_x, pos_y=pos_y)
        self._add_widget(text_widget, redraw)

        return text_widget

    # Image Button Related Functionality
    def image_button_id_available(self, button_id):
        return _form_full_widget_id(button_id, WidgetType.BUTTON) not in self.widgets

    def add_image_button(self, *, button_id, pos_x, pos_y, orig_on_release, images, current_image=1, redraw=True):
        if orig_on_release:
            button_type = ButtonType.RELEASE
        else:
            button_type = ButtonType.SWITCH
        button_widget = CanvasImageButton(button_id=button_id, button_type=button_type, pos_x=pos_x, pos_y=pos_y,
                                          image_list=images, current_image=current_image)
        self._add_widget(button_widget, redraw)

        return button_widget

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


def _form_full_widget_id(widget_id, widget_type):
    return widget_type.value + '_' + widget_id


def load_json(file_path):
    with open(file_path) as file_ptr:
        return json.load(file_ptr)


def dump_json(file_path, config):
    with open(file_path, 'w') as file_ptr:
        json.dump(config, file_ptr, indent=4)
