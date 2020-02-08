import os
import tkinter as tk
from tkinter import filedialog


class ImgEditor():  # pylint: disable=too-few-public-methods
    def __init__(self, root, working_dir):
        self.root_window = root
        self.working_dir = working_dir

        # Draw the Menu Bar
        self._draw_menu()

    def _draw_menu(self):
        menubar = tk.Menu(self.root_window)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Exit', command=self.root_window.quit)
        menubar.add_cascade(label='File', menu=file_menu)
        self.root_window.config(menu=menubar)


def ask_directory(title):
    return filedialog.askdirectory(title=title, initialdir=os.curdir)


def main():
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
