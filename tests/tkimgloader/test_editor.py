from tkinter import filedialog

from tkimgloader.editor import ImgEditor

SAMPLE_DIR = R'C:\Projects\This Project'

def test_editor_init_get_root_dir(monkeypatch):
    def mockreturn(*, title, initialdir):
        return SAMPLE_DIR
    monkeypatch.setattr(filedialog, 'askdirectory', mockreturn)

    editor = ImgEditor('fake_root')
    assert editor.root_window == 'fake_root'
    assert editor.working_dir == SAMPLE_DIR
