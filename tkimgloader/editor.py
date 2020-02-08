import os
import tkinter as tk
from tkinter import filedialog


class ImgEditor():
    def __init__(self, root):
        self.root_window = root
        self.working_dir = None

        # Ask for the Root Directory
        self.working_dir = self._get_working_dir()

    def _get_working_dir(self):
        return filedialog.askdirectory(title='Select the working directory', initialdir=os.curdir)


def main():
    root = tk.Tk()
    ImgEditor(root)
    root.mainloop()


if __name__ == '__main__':
    main()
