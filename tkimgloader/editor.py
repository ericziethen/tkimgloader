
import logging
import os

from functools import partial

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
import tkinter.simpledialog as simpledialog

import project_logger
from imgloader import ConfigDrawer
from widgets import WidgetType

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

NAV_DIRECTIONS = [
    ('▲', 0, -1),
    ('▼', 0, 1),
    ('◀', -1, 0),
    ('▶', 1, 0)]


class ImgEditor():
    def __init__(self, root, working_dir):
        logger.debug(F'Working Dir: {working_dir}')
        self.root_window = root
        self.working_dir = working_dir
        self.canvas = None
        self.columnspan = 20

        self.menu_widgets = []

        # Init the Canvas
        self._init_canvas()

        # Init the Config Drawer
        self.img_loader = ConfigDrawer(self.canvas)

        # Draw the Menu Bar
        self._draw_menu()

        # draw the text options
        self._draw_navigation_options()

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
        menubar.add_command(label='+ Text', command=self.add_text)
        menubar.add_command(label='+ Image Button', command=self.add_image_button)
        menubar.add_command(label='+ Input Box', command=self.add_input_box)

        if not self.img_loader.background_path:
            menubar.entryconfig('+ Text', state="disabled")
            menubar.entryconfig('+ Image Button', state="disabled")
            menubar.entryconfig('+ Input Box', state="disabled")

        self.root_window.config(menu=menubar)

        # Set our job to refresh screen data
        self.root_window.after(1000, self._refresh_screen_data)

    def _draw_navigation_options(self):  # pylint: disable=too-many-locals
        # Remove existing frames to redraw
        for menu_widget in self.menu_widgets:
            menu_widget.destroy()

        row = 0
        for widget in self.img_loader.widgets.values():
            row += 1
            col = 0

            frame = tk.Frame(self.root_window, width=self.root_window.winfo_width(),
                             bg="SystemButtonFace", colormap="new")
            frame.grid(row=row, columnspan=self.columnspan, sticky=tk.NSEW)

            # Widget Description
            text_col_span = 4
            main_text = tk.Label(frame, text=str(widget), anchor=tk.W)
            main_text.grid(row=row, column=col, columnspan=text_col_span, sticky=tk.W)
            frame.grid_columnconfigure(col, weight=2)
            col += text_col_span

            # Image Button Specific Menus
            if widget.widget_type == WidgetType.BUTTON:
                button = tk.Button(
                    frame, borderwidth=1, text='+ Img',
                    command=partial(self.add_image_to_button, widget))
                button.grid(row=row, column=col, sticky=tk.NSEW)
                col += 1

                button = tk.Button(
                    frame, borderwidth=1, text='- Img',
                    command=partial(self.remove_current_image, widget))
                button.grid(row=row, column=col, sticky=tk.NSEW)
                col += 1

            # Input box Specific
            if widget.widget_type == WidgetType.INPUT_BOX:
                def test_inputbox_callback(*, widget, text):
                    logger.info(F'Callback called for Input Box "{widget}" with value "{text}"')
                widget.add_callback(input_confirm_callback=test_inputbox_callback)

                button = tk.Button(
                    frame, borderwidth=1, text='Width',
                    command=partial(self.set_input_box_width, widget))
                button.grid(row=row, column=col, sticky=tk.NSEW)
                col += 1

            # Adding/Removing Labels
            if not widget.label:
                button = tk.Button(
                    frame, borderwidth=1, text='+ Label',
                    command=partial(self.add_widget_label, widget))
            else:
                button = tk.Button(
                    frame, borderwidth=1, text=F'- Label',
                    command=partial(self.remove_widget_label, widget))

            button.grid(row=row, column=col, sticky=tk.NSEW)
            col += 1

            # Text Moving Navigation
            nav_intervals = [50, 10, 1]
            for interval in nav_intervals:
                # Large Nav Text
                label = tk.Label(frame, text=F'Move {interval}')
                label.grid(row=row, column=col, sticky=tk.NSEW)
                col += 1

                # Large Nav Buttons
                for direction in NAV_DIRECTIONS:
                    button = tk.Button(
                        frame, borderwidth=1, text=direction[0],
                        command=partial(
                            self.move_widget_by,
                            direction[1] * interval,
                            direction[2] * interval,
                            widget=widget,
                            main_text_label=main_text))
                    button.grid(row=row, column=col, sticky=tk.NSEW)
                    col += 1

            # Remove Button
            remove_button = tk.Button(
                frame, borderwidth=1, text='Del',
                command=partial(self.remove_widget, widget))
            remove_button.grid(row=row, column=col, sticky=tk.NSEW)
            row += 1

            self.menu_widgets.append(frame)

            # Draw the separatpr
            sep = ttk.Separator(self.root_window, orient=tk.HORIZONTAL)
            sep.grid(column=0, row=row, columnspan=self.columnspan, sticky='ew')

            self.menu_widgets.append(sep)

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
                self._draw_navigation_options()

    def _save_config(self):
        config_path = self.img_loader.config_path
        if not config_path:
            config_path = filedialog.asksaveasfilename(
                title='Select File to Save', initialdir=self.working_dir,
                filetypes=(('Save Config', '.json'),))

        if config_path:
            if not config_path.lower().endswith('.json'):
                config_path += '.json'
            self.img_loader.save_config_to_file(config_path)

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

    def move_widget_by(self, move_x, move_y, *, widget, main_text_label):  # pylint: disable=no-self-use
        widget.move_by(move_x=move_x, move_y=move_y)
        main_text_label.config(text=str(widget))

    def remove_widget(self, widget):
        self.img_loader.remove_widget(widget)
        self._draw_navigation_options()

    def add_widget_label(self, widget):
        answer = simpledialog.askstring("Input", "Enter Widget Label",
                                        parent=self.root_window)

        if answer:
            widget.label = answer

            # Draw Editor Parts
            self._draw_navigation_options()

    def remove_widget_label(self, widget):
        widget.label = None
        self._draw_navigation_options()

    # Text Related Options
    def add_text(self):
        answer = simpledialog.askstring("Input", "Enter the text to add",
                                        parent=self.root_window)
        if answer:
            self.img_loader.add_text(text=answer, pos_x=100, pos_y=100)

            # Draw Editor Parts
            self._draw_navigation_options()

    # Button Related Data
    def add_image_button(self):

        # Ask if a Button or Switch
        button_or_switch = messagebox.askyesno("Question", "Is this a Button (Otherwise Switch)?")

        # Ask for the Button Image
        file_path_tuple = ask_multi_image_filepath('Select the Button Images', self.working_dir)
        if file_path_tuple:
            img_list = [self._get_rel_path(file_path) for file_path in file_path_tuple]
            button = self.img_loader.add_image_button(
                pos_x=100, pos_y=200, orig_on_release=button_or_switch, images=img_list)

            def test_release_callback(*, widget):
                logger.info(F'Callback called for Button "{widget}"')

            button.add_image_callback(button_release_func=test_release_callback)

            # Draw Editor Parts
            self._draw_navigation_options()

        else:
            messagebox.showerror('Error', F'At least 1 image needs to be selected')

    def add_image_to_button(self, widget):
        file_path_tuple = ask_multi_image_filepath('Select the Button Images', self.working_dir)
        if file_path_tuple:
            img_list = [self._get_rel_path(file_path) for file_path in file_path_tuple]
            widget.add_new_images(img_list)

    def remove_current_image(self, widget):
        try:
            deleted = widget.remove_current_image()
            if deleted:
                self._draw_navigation_options()
        except ValueError as error:
            messagebox.showerror('Warning', error)

    # Input Box Related Options
    def add_input_box(self):
        width = simpledialog.askinteger(
            'Input', 'Input Box Width?', parent=self.root_window, minvalue=0)

        if width:
            self.img_loader.add_input_box(pos_x=100, pos_y=100, width=width)

            # Draw Editor Parts
            self._draw_navigation_options()

    def set_input_box_width(self, widget):
        width = simpledialog.askinteger(
            'Input', 'New Input Box Width?', parent=self.root_window, minvalue=0)

        if width:
            widget.width = width

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


def ask_multi_image_filepath(title, initial_dir):
    return filedialog.askopenfilenames(
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
