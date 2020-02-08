import os
import tkinter as tk
from tkinter import filedialog


class ImgEditor():  # pylint: disable=too-few-public-methods
    def __init__(self, root):
        self.root_window = root
        self.working_dir = None

        # Ask for the Root Directory
        self.working_dir = ask_directory('Select the working directory')


def ask_directory(title):
    return filedialog.askdirectory(title=title, initialdir=os.curdir)


def main():
    root = tk.Tk()
    ImgEditor(root)
    root.mainloop()


if __name__ == '__main__':
    main()
