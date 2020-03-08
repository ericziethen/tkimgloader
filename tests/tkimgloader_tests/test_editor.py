import os

from tkinter import filedialog

import tkimgloader.editor as editor

SAMPLE_DIR = R'C:\Projects\This Project'
REL_FILE_PATH = R'SubDir\File.json'
SAMPLE_FILE = os.path.join(SAMPLE_DIR, REL_FILE_PATH)


'''


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!! DEFINE NEW TESTS BASED ON CODE






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

    assert editor.ask_image_filepath('Title', 'Initial Dir') == SAMPLE_FILE


def test_rel_path(monkeypatch):
    editor_init_mock_returns(monkeypatch)
    def mockreturn_openfile(**kwargs):
        return SAMPLE_FILE
    monkeypatch.setattr(filedialog, 'askopenfilename', mockreturn_openfile)

    edit = editor.ImgEditor('fake_root', SAMPLE_DIR)
    assert edit._get_rel_path(SAMPLE_FILE) == REL_FILE_PATH
'''