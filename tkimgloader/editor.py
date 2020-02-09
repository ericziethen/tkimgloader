
import logging
import os

import tkinter as tk
from tkinter import filedialog

from PIL import ImageTk

import project_logger

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ImgEditor():  # pylint: disable=too-few-public-methods
    def __init__(self, root, working_dir):
        logger.debug(F'Working Dir: {working_dir}')
        self.root_window = root
        self.working_dir = working_dir
        self.columnspan = 20

        self.images = {}

        self.img_config = {}

        # Init the Canvas
        self.canvas = tk.Canvas(self.root_window)
        self.canvas.grid(row=0, columnspan=self.columnspan)

        # Draw the Menu Bar
        self._draw_menu()

        # Draw the Content Screen
        self._draw_content()

    def _draw_menu(self):
        logger.debug(F'Drawing Menu')

        menubar = tk.Menu(self.root_window)
        file_menu = tk.Menu(menubar, tearoff=0)

        # Load Background
        file_menu.add_command(label='Select Background', command=self._open_background_image)

        # Exit
        file_menu.add_command(label='Exit', command=self.root_window.quit)

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
            self.img_config['background'] = os.path.join(self.working_dir, file_path)
            self._draw_content()


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
    if working_dir:
        root.deiconify()
        ImgEditor(root, working_dir)
        root.mainloop()
    else:
        root.quit()


if __name__ == '__main__':
    main()
