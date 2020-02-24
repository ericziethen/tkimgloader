
import datetime
import logging
import os

from functools import partial

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
import tkinter.simpledialog as simpledialog

import project_logger
from imgloader import ConfigDrawer

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ImgEditor():
    def __init__(self, root, working_dir):
        logger.debug(F'Working Dir: {working_dir}')
        self.root_window = root
        self.working_dir = working_dir
        self.canvas = None
        self.columnspan = 20

        self.text_frames = {}

        # Init the Canvas
        self._init_canvas()

        # Init the Config Drawer
        self.img_loader = ConfigDrawer(self.canvas)

        # Draw the Menu Bar
        self._draw_menu()

        # draw the text options
        self._draw_text_options()

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

        # Set our job to refresh screen data
        self.root_window.after(1000, self._refresh_screen_data)

    def _draw_text_options(self):  # pylint: disable=too-many-locals
        logger.debug(F'Drawing Text Options for: {self.img_loader.config["text"]}')

        # Remove existing frames to redraw
        for frame in self.text_frames.values():
            frame.destroy()

        directions = [
            ('▲', 0, -1),
            ('▼', 0, 1),
            ('◀', -1, 0),
            ('▶', 1, 0)]

        row = 0
        for count, (text_id, _) in enumerate(self.img_loader.config['text'].items()):
            row += 1
            col = 0

            # Draw the separatpr
            if count > 0:
                sep = ttk.Separator(self.root_window, orient=tk.HORIZONTAL)
                sep.grid(column=0, row=row, columnspan=self.columnspan, sticky='ew')
                row += 1

            frame = tk.Frame(self.root_window, width=self.root_window.winfo_width(),
                             bg="SystemButtonFace", colormap="new")
            frame.grid(row=row, columnspan=self.columnspan, sticky=tk.NSEW)

            # Actual Text
            text_col_span = 4
            main_text = tk.Label(frame, text=self.form_text_bar_label(text_id), anchor="w")
            main_text.grid(row=row, column=col, columnspan=text_col_span, sticky=tk.W)
            frame.grid_columnconfigure(col, weight=1)
            col += text_col_span

            # Text Moving Navigation
            nav_intervals = [50, 10, 1]
            for interval in nav_intervals:
                # Large Nav Text
                label = tk.Label(frame, text=F'Move {interval}')
                label.grid(row=row, column=col, sticky=tk.NSEW)
                col += 1

                # Large Nav Buttons
                for direction in directions:
                    button = tk.Button(
                        frame, borderwidth=1, text=direction[0],
                        command=partial(
                            self.move_text, text_id,
                            direction[1] * interval,
                            direction[2] * interval,
                            main_text_label=main_text))
                    button.grid(row=row, column=col, sticky=tk.NSEW)
                    col += 1

            # Remove Button
            remove_button = tk.Button(frame, borderwidth=1, text='Remove',
                                      command=partial(self.remove_text, text_id))
            remove_button.grid(row=row, column=col, sticky=tk.NSEW)

            self.text_frames[text_id] = frame

    def _open_background_image(self):
        file_path = ask_image_filepath('Select the Background Image', self.working_dir)
        if file_path:
            logger.debug(F'Filepath Selected: "{file_path}""')
            rel_path = self._get_rel_path(file_path)
            logger.debug(F'Rel Filepath Selected: "{rel_path}"')
            self.img_loader.load_background(rel_path)
            self._draw_menu()  # To enable Insert Box

    def _load_config(self):
        can_load = True
        if self.img_loader.unsaved_changes:
            if not messagebox.askyesno('Unsaved Changes', 'Load Config without saving?'):
                can_load = False

        if can_load:
            config_path = filedialog.askopenfilename(
                title='Select File to Save', initialdir=self.working_dir,
                filetypes=(('Save Config', '.json'),))
            if config_path:
                self.img_loader.load_config_file(config_path)

                # Draw Editor Parts
                self._draw_menu()  # To enable Insert Box
                self._draw_text_options()

    def _save_config(self):
        config_path = self.img_loader.config_path
        if not config_path:
            config_path = filedialog.asksaveasfilename(
                title='Select File to Save', initialdir=self.working_dir,
                filetypes=(('Save Config', '.json'),))

        if config_path:
            if not config_path.lower().endswith('.json'):
                config_path += '.json'
            self.img_loader.save_config(config_path)

    def _get_rel_path(self, path):
        return os.path.relpath(path, self.working_dir)

    def exit(self):
        can_exit = True

        if self.img_loader.unsaved_changes:
            if not messagebox.askyesno('Unsaved Changes', 'Exit without Saving?'):
                can_exit = False

        if can_exit:
            logger.debug('Exit Application')
            self.root_window.quit()

    # Text Related Options
    def add_text(self):
        answer = simpledialog.askstring("Input", "Enter the text to add",
                                        parent=self.root_window)
        if answer:
            key = str(datetime.datetime.now())
            self.img_loader.add_text(text_id=key, text=answer, pos_x=100, pos_y=100)

            # Draw Editor Parts
            self._draw_text_options()

    def move_text(self, idx, move_x, move_y, *, main_text_label):
        self.img_loader.move_text(text_id=idx, move_x=move_x, move_y=move_y)
        main_text_label.config(text=self.form_text_bar_label(idx))

    def remove_text(self, idx):
        logger.debug(F'Config Before Removal: {self.img_loader.config}')
        self.img_loader.remove_text(text_id=idx)
        logger.debug(F'Config After Removal: {self.img_loader.config}')
        self._draw_text_options()

    def form_text_bar_label(self, text_id):
        text_details = self.img_loader.config['text'][text_id]
        return F'{text_details["text"]} [{text_details["x"]},{text_details["y"]}]'

    # Button Related Data





    def _refresh_screen_data(self):
        # https://riptutorial.com/tkinter/example/22870/-after--

        dims = self.img_loader.dimensions
        resolution = F'{dims[0]} x {dims[1]}'

        self.root_window.title(F'Resolution: {resolution}, Config: "{self.img_loader.config_path}"')

        self.root_window.after(1000, self._refresh_screen_data)


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
