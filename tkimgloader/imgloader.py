
import copy
import json
import logging

import tkinter as tk

from PIL import ImageTk

from tkimgloader.widgets import ButtonType, CanvasImageButton, CanvasText, InputBox

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ConfigDrawer():  # pylint: disable=too-many-public-methods
    def __init__(self, canvas):
        self.canvas = canvas
        self.config_path = None
        self.background_path = None
        self.widgets = {}
        self.images = {}
        self.saved_img_config = self.calc_config_dict()

    @property
    def unsaved_changes(self):
        return self.calc_config_dict() != self.saved_img_config

    @property
    def dimensions(self):
        if 'background' in self.images:
            return (self.images['background'].width(), self.images['background'].height())
        return (0, 0)

    def __eq__(self, other):
        if self.calc_config_dict() != other.calc_config_dict():
            return False

        return True

    def get_widget_with_label(self, label):
        for widget in self.widgets.values():
            if label == widget.label:
                return widget
        return None

    def _add_widget(self, widget, draw=True):
        if widget.label and self.get_widget_with_label(widget.label) is not None:
            raise ValueError('Cannot have 2 Widgets with Identical Labels')

        widget_id = id(widget)

        self.widgets[widget_id] = widget
        if draw:
            widget.canvas = self.canvas
            self.widgets[widget_id].draw()

    def remove_widget(self, widget, draw=True):
        widget_id = id(widget)

        if draw:
            self.widgets[widget_id].destroy()
        del self.widgets[widget_id]

    def load_background(self, path, draw=True):
        self.background_path = path

        if draw:
            logger.debug(F'Drawing Background file "{path}"')

            background = ImageTk.PhotoImage(file=path)
            self.images['background'] = background

            self.canvas.config(width=background.width(), height=background.height())
            self.canvas.create_image(0, 0, image=background, anchor=tk.NW)

    def calc_config_dict(self):
        config = {}

        config['background'] = self.background_path

        for widget in self.widgets.values():
            widget_type = widget.widget_type
            if widget_type.value not in config:
                config[widget_type.value] = []
            config[widget_type.value].append(widget.to_dict())

        return config

    def _load_config(self, config, *, config_path, draw=True):
        # Set config vars
        self.config_path = config_path

        # Load the background
        if 'background' in config:
            self.load_background(config['background'], draw=draw)

        # Load the Text Items
        if 'Text' in config:
            for text_item in config['Text']:
                self.add_text(label=text_item['label'], text=text_item['text'],
                              pos_x=text_item['x'], pos_y=text_item['y'], draw=draw)

        # Load the image button items
        if 'Button' in config:
            for button_dic in config['Button']:
                self.add_image_button(label=button_dic['label'], pos_x=button_dic['x'], pos_y=button_dic['y'],
                                      orig_on_release=button_dic['orig_image_on_release'],
                                      current_image=button_dic['current_image'],
                                      images=list(button_dic['images'].values()), draw=draw)

        # Load Input Boxes
        if 'Input Box' in config:
            for text_item in config['Input Box']:
                self.add_input_box(label=text_item['label'], pos_x=text_item['x'], pos_y=text_item['y'], draw=draw)

        self.saved_img_config = self.calc_config_dict()

    def load_config_file(self, config_path, *, draw=True):
        config = load_json(config_path)
        logger.debug(F'Load Config: {config}')
        self._load_config(config, config_path=config_path, draw=draw)

    def save_config_to_file(self, config_path):
        config = self.calc_config_dict()
        dump_json(config_path, config)
        self.config_path = config_path
        self.saved_img_config = copy.deepcopy(config)

    def add_text(self, *, label=None, text, pos_x, pos_y, draw=True):
        text_widget = CanvasText(label=label, text=text, pos_x=pos_x, pos_y=pos_y)
        self._add_widget(text_widget, draw)

        return text_widget

    def add_image_button(self, *, label=None, pos_x, pos_y, orig_on_release, images, current_image=1, draw=True):
        if orig_on_release:
            button_type = ButtonType.RELEASE
        else:
            button_type = ButtonType.SWITCH
        button_widget = CanvasImageButton(label=label, button_type=button_type, pos_x=pos_x, pos_y=pos_y,
                                          image_list=images, current_image=current_image)
        self._add_widget(button_widget, draw)

        return button_widget

    def add_input_box(self, *, label=None, pos_x, pos_y, width=None, draw=True):
        widget = InputBox(label=label, pos_x=pos_x, pos_y=pos_y, width=width)
        self._add_widget(widget, draw)

        return widget


def load_json(file_path):
    with open(file_path) as file_ptr:
        return json.load(file_ptr)


def dump_json(file_path, config):
    with open(file_path, 'w') as file_ptr:
        json.dump(config, file_ptr, indent=4)
