
import enum
import tkinter as tk

from PIL import ImageTk


@enum.unique
class WidgetType(enum.Enum):
    # pylint: disable=invalid-name
    BUTTON = 'Button'
    TEXT = 'Text'


@enum.unique
class ButtonType(enum.Enum):
    # pylint: disable=invalid-name
    RELEASE = 'Release'
    SWITCH = 'Switch'


class Widget():
    def __init__(self, *, widget_type, pos_x, pos_y):
        # Set Attributes
        self.canvas = None
        self.widget_type = widget_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.canvas_widget = None

    @property
    def widget_type(self):
        return self._widget_type

    @widget_type.setter
    def widget_type(self, widget_type):
        if not isinstance(widget_type, WidgetType):
            raise ValueError(F'Invalid type " {widget_type}" Passed, not of type WidgetType')
        self._widget_type = widget_type

    def __str__(self):
        return F'({self.widget_type.value}) [{self.pos_x},{self.pos_y}]'

    def to_dict(self):
        return {'x': self.pos_x, 'y': self.pos_y}

    def draw(self):
        raise NotImplementedError

    def destroy(self):
        self.canvas.delete(self.canvas_widget)

    def move_to(self, *, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.redraw_widget()

    def move_by(self, *, move_x, move_y):
        self.move_to(pos_x=self.pos_x + move_x, pos_y=self.pos_y + move_y)

    def redraw_widget(self):
        if self.canvas:
            self.canvas.coords(self.canvas_widget, self.pos_x, self.pos_y)


class CanvasText(Widget):
    def __init__(self, *, text, pos_x, pos_y):
        self.text = text
        super().__init__(pos_x=pos_x, pos_y=pos_y, widget_type=WidgetType.TEXT)

    def __str__(self):
        return F'{self.text} {super().__str__()}'

    def to_dict(self):
        data_dict = super().to_dict()
        data_dict['text'] = self.text
        return data_dict

    def draw(self):
        if self.canvas:
            self.canvas_widget = self.canvas.create_text(self.pos_x, self.pos_y, text=self.text, anchor=tk.NW,
                                                         font='Times 10 italic bold')


class CanvasImageButton(Widget):
    def __init__(self, *, button_type, pos_x, pos_y, image_list, current_image=1):
        if not image_list:
            raise ValueError('Image list cannot be empty')

        super().__init__(pos_x=pos_x, pos_y=pos_y, widget_type=WidgetType.BUTTON)
        self.button_type = button_type
        self.image_path_dic = dict(enumerate(image_list, start=1))
        self.current_image = current_image
        self.images = {}
        self.release_callback = None

    @property
    def button_type(self):
        return self._button_type

    @button_type.setter
    def button_type(self, button_type):
        if not isinstance(button_type, ButtonType):
            raise ValueError(F'Invalid type " {button_type}" Passed, not of type ButtonType')
        self._button_type = button_type

    def __str__(self):
        return F'{self.button_type.value} {super().__str__()}'

    def to_dict(self):
        data_dict = super().to_dict()
        data_dict['orig_image_on_release'] = self.button_type == ButtonType.RELEASE
        data_dict['current_image'] = self.current_image
        data_dict['images'] = self.image_path_dic
        return data_dict

    def draw(self):
        if self.canvas:
            # Setup all images
            for img_path in self.image_path_dic.values():
                if img_path not in self.images:
                    self.images[img_path] = ImageTk.PhotoImage(file=img_path)

            # Draw the current image
            current_img_path = self.image_path_dic[self.current_image]
            current_img = self.images[current_img_path]

            self.canvas_widget = self.canvas.create_image(self.pos_x, self.pos_y, image=current_img)

            self.canvas.tag_bind(self.canvas_widget, '<Button-1>', self.button_pressed)
            self.canvas.tag_bind(self.canvas_widget, '<ButtonRelease-1>', self.button_released)

            self.canvas.tag_bind(self.canvas_widget, '<Button-3>', self.button_pressed)
            self.canvas.tag_bind(self.canvas_widget, '<ButtonRelease-3>', self.button_released)

    def button_pressed(self, event):
        if (event.num == 1) and (self.button_type == ButtonType.RELEASE):
            self.next_image()

    def button_released(self, event):
        if event.num == 1:
            if self.button_type == ButtonType.RELEASE:
                self.previous_image()
            else:
                self.next_image()
        elif (self.button_type == ButtonType.SWITCH) and (event.num == 3):
            self.previous_image()

        if self.release_callback:
            self.release_callback(widget=self)

    def next_image(self):
        previous_image = self.current_image
        if len(self.image_path_dic) > self.current_image:
            self.current_image += 1
        else:
            self.current_image = 1

        if previous_image != self.current_image:
            img_path = self.image_path_dic[self.current_image]
            if self.canvas:
                self.canvas.itemconfig(self.canvas_widget, image=self.images[img_path])

    def previous_image(self):
        previous_image = self.current_image
        if self.current_image > 1:
            self.current_image -= 1
        else:
            self.current_image = len(self.image_path_dic)

        if previous_image != self.current_image:
            img_path = self.image_path_dic[self.current_image]
            if self.canvas:
                self.canvas.itemconfig(self.canvas_widget, image=self.images[img_path])

    def add_new_images(self, path_list):
        for image_path in path_list:
            if image_path not in self.images:
                self.images[image_path] = ImageTk.PhotoImage(file=image_path)

        new_path_list = list(self.image_path_dic.values())
        new_path_list = (new_path_list[:self.current_image] +
                         path_list + new_path_list[self.current_image:])

        self.image_path_dic = dict(enumerate(new_path_list, start=1))
        self.next_image()

    def remove_current_image(self):
        if len(self.image_path_dic) == 1:
            raise ValueError('Cannot delete the last image')

        image_to_delete = self.current_image

        # Set the previous image as the current one
        self.previous_image()

        # Remove the Image
        del self.image_path_dic[image_to_delete]

        # Reindex the remaining images
        self.image_path_dic = dict(enumerate(self.image_path_dic.values(), start=1))

        # Set the new Current Image, deleted after gone to previous so might be out of step
        if image_to_delete > 1:
            self.current_image = image_to_delete - 1
        else:
            self.current_image = len(self.image_path_dic)

    def add_image_callback(self, *, button_release_func):
        self.release_callback = button_release_func
