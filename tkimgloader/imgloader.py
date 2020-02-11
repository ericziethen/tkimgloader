
import json
import logging

import tkinter as tk

from PIL import ImageTk

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ConfigDrawer():
    def __init__(self, canvas):
        self.canvas = canvas
        self._config = {}
        self.images = {}
        self.config_path = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config
        self.draw()

    @config.setter
    def background(self, file_path):
        self.config['background'] = file_path
        self.draw()

    def draw(self):
        logger.debug(F'Drawing Content: {self.config}')

        # Draw the Background
        if 'background' in self.config:
            img_path = self.config['background']
            logger.debug(F'Drawing Background file "{img_path}"')

            background = ImageTk.PhotoImage(file=img_path)
            self.images['background'] = background  # Make the image persistent

            self.canvas.config(width=background.width(), height=background.height())
            self.canvas.create_image(0, 0, image=background, anchor=tk.NW)
        else:
            logger.debug('No Background to Draw')

    def load_config(self, config_path):
        with open(config_path) as file_ptr:
            self.config = json.load(file_ptr)

    def save_config(self, config_path):
        with open(config_path, 'w') as file_ptr:
            json.dump(self.config, file_ptr, indent=4)

    def add_text(self, *, text_id, text, pos_x, pos_y):
        if 'text' not in self.config:
            self.config['text'] = {}
        self.config['text'][text_id] = {'text': text, 'x': pos_x, 'y': pos_y}
        self.draw()

    def remove_text(self, *, text_id):
        del self.config['text'][text_id]
