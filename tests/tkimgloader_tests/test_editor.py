import os

from tkinter import filedialog

import tkimgloader.scripts.editor as editor

SAMPLE_DIR = R'C:\Projects\This Project'
REL_FILE_PATH = R'SubDir\File.json'
SAMPLE_FILE = os.path.join(SAMPLE_DIR, REL_FILE_PATH)


def editor_init_mock_returns(monkeypatch):
    def mockreturn(mockself):
        return None
    monkeypatch.setattr(editor.ImgEditor, '_init_canvas', mockreturn)
    monkeypatch.setattr(editor.ImgEditor, '_draw_menu', mockreturn)


def test_ask_directory(monkeypatch):
    def mockreturn(*, title, initialdir):
        return SAMPLE_DIR
    monkeypatch.setattr(filedialog, 'askdirectory', mockreturn)

    assert editor.ask_directory('Title') == SAMPLE_DIR


def test_editor_init(monkeypatch):
    editor_init_mock_returns(monkeypatch)

    edit = editor.ImgEditor('fake_root', SAMPLE_DIR)
    assert edit.root_window == 'fake_root'
    assert edit.working_dir == SAMPLE_DIR


def test_ask_file(monkeypatch):
    def mockreturn(**kwargs):
        return SAMPLE_FILE
    monkeypatch.setattr(filedialog, 'askopenfilename', mockreturn)

    assert editor.ask_image_filepath('Title', SAMPLE_DIR) == REL_FILE_PATH
