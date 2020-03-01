

'''
def test_text_added_in_config():
    drawer = ConfigDrawer('fake_canvas')

    text = Text(id='id', text='sample_text', pos_x=100, pos_y=200)
    drawer.add_widget(text)

    assert 'text' in drawer.config
    assert 'id' in drawer.config['text']
    assert drawer.config['text']['id']['text'] == 'sample_text'
    assert drawer.config['text']['id']['x'] == 100
    assert drawer.config['text']['id']['y'] == 200
    assert 'id' in drawer.canvas_text_details
'''