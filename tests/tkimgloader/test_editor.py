from tkinter import filedialog

import tkimgloader.editor as editor

SAMPLE_DIR = R'C:\Projects\This Project'

def test_ask_directory(monkeypatch):
    def mockreturn(*, title, initialdir):
        return SAMPLE_DIR
    monkeypatch.setattr(filedialog, 'askdirectory', mockreturn)

    assert editor.ask_directory('Title') == SAMPLE_DIR

def test_editor_init_get_root_dir(monkeypatch):
    def mockreturn(*, title, initialdir):
        return SAMPLE_DIR
    monkeypatch.setattr(filedialog, 'askdirectory', mockreturn)

    edit = editor.ImgEditor('fake_root')
    assert edit.root_window == 'fake_root'
    assert edit.working_dir == SAMPLE_DIR
