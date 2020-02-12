
import json
import logging

import tkinter as tk

from PIL import ImageTk

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ConfigDrawer():
    def __init__(self, canvas):
        self.canvas = canvas
        self.config = {'background': None, 'text': {}}
        self.images = {}
        self.config_path = None

    @property
    def background(self):
        return self.config['background']

    @background.setter
    def background(self, file_path):
        self.config['background'] = file_path
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

        # Draw the Text
        if 'text' in self.config and self.config['text']:
            for _, text_dict in self.config['text'].items():
                logger.debug(F'''Create Text "{text_dict['text']}" @ {text_dict['x']}x{text_dict['y']}''')
                test = self.canvas.create_text(
                    text_dict['x'], text_dict['y'], anchor=tk.NW,
                    font="Times 10 italic bold", text=text_dict['text'])

    def load_config(self, config_path):
        with open(config_path) as file_ptr:
            self.config = json.load(file_ptr)
            self.draw()

    def save_config(self, config_path):
        with open(config_path, 'w') as file_ptr:
            json.dump(self.config, file_ptr, indent=4)

    def add_text(self, *, text_id, text, pos_x, pos_y):
        self.config['text'][text_id] = {'text': text, 'x': pos_x, 'y': pos_y}
        self.draw()

    def update_text(self, *, text_id, pos_x, pos_y):
        self.config['text'][text_id]['x'] = pos_x
        self.config['text'][text_id]['y'] = pos_y
        self.draw()

    def move_text(self, *, text_id, move_x, move_y):
        self.update_text(
            text_id=text_id,
            pos_x=self.config['text'][text_id]['x'] + move_x,
            pos_y=self.config['text'][text_id]['y'] + move_y)

    def remove_text(self, *, text_id):
        del self.config['text'][text_id]
        self.draw()
