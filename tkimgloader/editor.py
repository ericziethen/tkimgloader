
import json
import logging
import os

import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import ImageTk

import project_logger

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ImgEditor():  # pylint: disable=too-few-public-methods
    def __init__(self, root, working_dir):
        logger.debug(F'Working Dir: {working_dir}')
        self.root_window = root
        self.working_dir = working_dir
        self.canvas = None
        self.columnspan = 20

        self.images = {}

        self.img_config = {}
        self.saved_img_config = {}
        self.config_path = None

        # Init the Canvas
        self._init_canvas()

        # Draw the Menu Bar
        self._draw_menu()

        # Draw the Content Screen
        self._draw_content()

    @property
    def unsaved_changes(self):
        return self.img_config != self.saved_img_config

    def _init_canvas(self):
        self.root_window.title(F'Config: N/A')
        self.canvas = tk.Canvas(self.root_window)
        self.canvas.grid(row=0, columnspan=self.columnspan)

    def _draw_menu(self):
        logger.debug(F'Drawing Menu')

        menubar = tk.Menu(self.root_window)
        file_menu = tk.Menu(menubar, tearoff=0)

        # Load Background
        file_menu.add_command(label='Select Background', command=self._open_background_image)
        file_menu.add_separator()

        # Load and Save config
        file_menu.add_command(label='Load Config', command=self._load_config)
        file_menu.add_command(label='Save Config', command=self._save_config)
        file_menu.add_separator()

        # Exit
        file_menu.add_command(label='Exit', command=self.exit)

        menubar.add_cascade(label='File', menu=file_menu)
        self.root_window.config(menu=menubar)

    def _draw_content(self):
        logger.debug(F'Drawing Content: {self.img_config}')

        # Draw the Background
        if 'background' in self.img_config:
            img_path = self.img_config['background']
            logger.debug(F'Drawing Background file "{img_path}"')

            background = ImageTk.PhotoImage(file=img_path)
            self.images['background'] = background  # Make the image persistent

            self.canvas.config(width=background.width(), height=background.height())

            self.canvas.create_image(0, 0, image=background, anchor=tk.NW)
        else:
            logger.debug('No Background to Draw')

    def _open_background_image(self):
        file_path = ask_image_filepath('Select the Background Image', self.working_dir)
        if file_path:
            logger.debug(F'Filepath Selected: "{file_path}""')
            rel_path = self._get_rel_path(file_path)
            logger.debug(F'Rel Filepath Selected: "{rel_path}"')
            self.img_config['background'] = rel_path
            self._draw_content()

    def _get_rel_path(self, path):
        return os.path.relpath(path, self.working_dir)

    def _load_config(self):
        can_load = True
        if self.unsaved_changes:
            if not messagebox.askyesno('Unsaved Changes', 'Load Config without saving?'):
                can_load = False

        if can_load:
            config_path = filedialog.askopenfilename(
                title='Select File to Save', initialdir=self.working_dir,
                filetypes=(('Save Config', '.json'),))
            if config_path:
                with open(config_path) as file_ptr:
                    self.img_config = json.load(file_ptr)
                    self.saved_img_config = self.img_config.copy()
                self._set_config_path(config_path)
                self._draw_content()

    def _save_config(self):
        config_path = self.config_path
        if not config_path:
            config_path = filedialog.asksaveasfilename(
                title='Select File to Save', initialdir=self.working_dir,
                filetypes=(('Save Config', '.json'),))

        if config_path:
            if not config_path.lower().endswith('.json'):
                config_path += '.json'
            with open(config_path, 'w') as file_ptr:
                json.dump(self.img_config, file_ptr, indent=4)
                self.saved_img_config = self.img_config.copy()
            self._set_config_path(config_path)

    def _set_config_path(self, path):
        self.config_path = self._get_rel_path(path)
        self.root_window.title(F'Config: "{self.config_path}"')

    def exit(self):
        can_exit = True
        if self.unsaved_changes:
            if not messagebox.askyesno('Unsaved Changes', 'Exit without Saving?'):
                can_exit = False

        if can_exit:
            logger.debug('Exit Application')
            self.root_window.quit()


def ask_directory(title):
    return filedialog.askdirectory(title=title, initialdir=os.curdir)


def ask_image_filepath(title, initial_dir):
    return filedialog.askopenfilename(
        title=title, initialdir=initial_dir,
        filetypes=(('Image files', '.bmp .gif .jpg .jpeg .png'),))


def main():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    project_logger.setup_logger(os.path.join(log_dir, 'debug.log'))

    root = tk.Tk()
    root.withdraw()

    # Ask for the Root Directory
    working_dir = ask_directory('Select the working directory')
    logger.debug('Working Dir Selected: "{working_dir}"')
    if working_dir:
        root.deiconify()
        ImgEditor(root, working_dir)
        root.mainloop()
    else:
        root.quit()


if __name__ == '__main__':
    main()
