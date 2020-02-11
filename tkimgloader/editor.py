

import datetime
import logging
import os

from functools import partial

import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.simpledialog as simpledialog

import project_logger
from imgloader import ConfigDrawer

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ImgEditor():  # pylint: disable=too-many-instance-attributes
    def __init__(self, root, working_dir):
        logger.debug(F'Working Dir: {working_dir}')
        self.root_window = root
        self.working_dir = working_dir
        self.canvas = None
        self.columnspan = 20
        self.large_pxl_move = 10

        self.saved_img_config = {}
        self.config_path = None

        # Init the Canvas
        self._init_canvas()

        # Init the Config Drawer
        self.img_loader = ConfigDrawer(self.canvas)

        # Draw the Menu Bar
        self._draw_menu()

        # draw the text options
        self._draw_text_options()

    # TODO - Does this still work?
    @property
    def unsaved_changes(self):
        return self.img_loader.config != self.saved_img_config

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
        menubar.add_command(label='Add Text', command=self.add_text)

        if not self.img_loader.background:
            menubar.entryconfig('Add Text', state="disabled")

        self.root_window.config(menu=menubar)

    def _draw_text_options(self):
        logger.debug(F'Drawing Text Options for', self.img_loader.config['text'])

        directions = [
            ('▲', 0, -1),
            ('▼', 0, 1),
            ('◀', -1, 0),
            ('▶', 1, 0),]

        for idx, (text_id, text_details) in enumerate(self.img_loader.config['text'].items()):
            text = text_details['text']

            row = col = 0

            # Actual Text
            label = tk.Label(self.root_window, text=F'{text} [{text_details["x"]},{text_details["y"]}]')
            label.grid(row=1, column=col)
            self.root_window.grid_columnconfigure(col, weight=1)
            col += 1

            # Large Nav Text
            label = tk.Label(self.root_window, text=F'Move {self.large_pxl_move}')
            label.grid(row=row, column=col)
            self.root_window.grid_columnconfigure(col, weight=1)
            col += 1

            # Large Nav Buttons
            for direction in directions:
                button = tk.Button(
                    self.root_window, borderwidth=1, text=direction[0],
                    command=partial(self.adjust_text, text, direction[1]*self.large_pxl_move, direction[2]*self.large_pxl_move))
                button.grid(row=row, column=col)
                col += 1

    def _open_background_image(self):
        file_path = ask_image_filepath('Select the Background Image', self.working_dir)
        if file_path:
            logger.debug(F'Filepath Selected: "{file_path}""')
            rel_path = self._get_rel_path(file_path)
            logger.debug(F'Rel Filepath Selected: "{rel_path}"')
            self.img_loader.background = rel_path
            self._draw_menu()  # To enable Insert Box

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
                self.img_loader.load_config(config_path)
                self.saved_img_config = self.img_loader.config.copy()
                self._set_window_title(config_path)

                # Draw Editor Parts
                self._draw_menu()  # To enable Insert Box
                self._draw_text_options()

    def _save_config(self):
        config_path = self.config_path
        if not config_path:
            config_path = filedialog.asksaveasfilename(
                title='Select File to Save', initialdir=self.working_dir,
                filetypes=(('Save Config', '.json'),))

        if config_path:
            if not config_path.lower().endswith('.json'):
                config_path += '.json'
            self.img_loader.save_config(config_path)
            self.saved_img_config = self.img_loader.config.copy()
            self._set_window_title(config_path)

    def _set_window_title(self, path):
        self.config_path = path
        self.root_window.title(F'Config: "{self.config_path}"')

    def _get_rel_path(self, path):
        return os.path.relpath(path, self.working_dir)

    def exit(self):
        can_exit = True
        if self.unsaved_changes:
            if not messagebox.askyesno('Unsaved Changes', 'Exit without Saving?'):
                can_exit = False

        if can_exit:
            logger.debug('Exit Application')
            self.root_window.quit()

    def add_text(self):
        answer = simpledialog.askstring("Input", "Enter the text to add",
                                        parent=self.root_window)
        if answer:
            key = str(datetime.datetime.now())
            self.img_loader.add_text(text_id=key, text=answer, pos_x=100, pos_y=100)

            # Draw Editor Parts
            self._draw_text_options()

    def move_text(self, idx, x, y):
        #- need to modify text - call update text methiod
        # TODO
        pass





def ask_directory(title):
    return filedialog.askdirectory(title=title, initialdir=os.curdir)


def ask_image_filepath(title, initial_dir):
    return filedialog.askopenfilename(
        title=title, initialdir=initial_dir,
        filetypes=(('Image files', '.bmp .gif .jpg .jpeg .png'),))


def main():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

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
