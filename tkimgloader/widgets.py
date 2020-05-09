
import enum
import tkinter as tk

from PIL import ImageTk


@enum.unique
class WidgetType(enum.Enum):
    # pylint: disable=invalid-name
    BUTTON = 'Button'
    TEXT = 'Text'
    INPUT_BOX = 'Input Box'
    TABLE = 'Table'


@enum.unique
class ButtonType(enum.Enum):
    # pylint: disable=invalid-name
    RELEASE = 'Release'
    SWITCH = 'Switch'


class Widget():
    def __init__(self, *, label=None, widget_type, pos_x, pos_y):
        # Set Attributes
        self.canvas = None
        self.label = label
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
        label_str = ''
        if self.label:
            label_str = F'[{self.label}]'

        return F'({self.widget_type.value}) {label_str}[{self.pos_x},{self.pos_y}]'

    def to_dict(self):
        return {'label': self.label, 'x': self.pos_x, 'y': self.pos_y}

    def draw(self):
        raise NotImplementedError

    def destroy(self):
        raise NotImplementedError

    def lift(self):
        raise NotImplementedError

    def move_to(self, *, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.redraw_widget()

    def move_by(self, *, move_x, move_y):
        self.move_to(pos_x=self.pos_x + move_x, pos_y=self.pos_y + move_y)

    def redraw_widget(self):
        raise NotImplementedError


class CanvasWidget(Widget):  # pylint: disable=abstract-method
    def destroy(self):
        self.canvas.delete(self.canvas_widget)

    def redraw_widget(self):
        if self.canvas:
            self.canvas.coords(self.canvas_widget, self.pos_x, self.pos_y)

    def lift(self):
        self.canvas.tag_raise(self.canvas_widget)


class FloatingWidget(Widget):  # pylint: disable=abstract-method
    def destroy(self):
        self.canvas_widget.destroy()

    def redraw_widget(self):
        if self.canvas:
            self.canvas_widget.place(x=self.pos_x, y=self.pos_y)

    def lift(self):
        self.canvas_widget.lift()


class CanvasText(CanvasWidget):
    def __init__(self, *, label=None, text, pos_x, pos_y):
        super().__init__(label=label, pos_x=pos_x, pos_y=pos_y, widget_type=WidgetType.TEXT)
        self.text = text

    def __setattr__(self, name, value):
        if name == 'text':
            super().__setattr__(name, value)
            if self.canvas_widget:
                self.redraw_widget()
        else:
            super().__setattr__(name, value)

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

    def redraw_widget(self):
        super().redraw_widget()
        if self.canvas:
            self.canvas.itemconfig(self.canvas_widget, text=self.text)


class CanvasImageButton(CanvasWidget):
    def __init__(self, *, label=None, button_type, pos_x, pos_y, image_list, current_image=1):
        if not image_list:
            raise ValueError('Image list cannot be empty')

        super().__init__(label=label, pos_x=pos_x, pos_y=pos_y, widget_type=WidgetType.BUTTON)
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


class CanvasTable(CanvasWidget):
    def __init__(self, *, label=None, pos_x, pos_y, column_widths, row_heights):
        super().__init__(label=label, pos_x=pos_x, pos_y=pos_y, widget_type=WidgetType.TABLE)
        self._column_widths = dict(enumerate(column_widths, start=1))
        self._row_heights = dict(enumerate(row_heights, start=1))

        # Setup the Grid
        self._widgets = []
        for _ in column_widths:
            self._widgets.append(self.get_empty_column())

    def get_empty_column(self):
        return [None for x in range(len(self._row_heights))]

    def _check_index(self, *, col, row):
        # Catch Negativ index errors as python will treat them from back of the list and will not be raised by access
        if col < 1 or row < 1:
            raise IndexError(F'Cannot have less than 1 as Table Index, have Column={col}, Row={row}')

    def add_widget(self, widget, *, col, row):
        if widget.widget_type not in [WidgetType.TEXT, WidgetType.BUTTON]:
            raise ValueError(F'Widget Type "{widget.widget_type}" not supported to add to a Table')
        self._check_index(col=col, row=row)

        self._widgets[col - 1][row - 1] = widget

    def get_widget(self, *, col, row):
        self._check_index(col=col, row=row)

        return self._widgets[col - 1][row - 1]

    def remove_widget(self, *, col, row):
        self._check_index(col=col, row=row)

        self._widgets[col - 1][row - 1] = None

    def add_row(self, *, row, height):
        # Update the heights
        heights = list(self._row_heights.values())
        heights.insert(row - 1, height)
        self._row_heights = dict(enumerate(heights, start=1))

        # shift the rows
        for col in self._widgets:
            col.insert(row - 1, None)

    def remove_row(self, *, row):
        # Update the heights
        heights = list(self._row_heights.values())
        del heights[row - 1]
        self._row_heights = dict(enumerate(heights, start=1))

        # shift the rows
        for col in self._widgets:
            del col[row - 1]

    def set_row_height(self, height, *, row):
        self._row_heights[row] = height

    def add_column(self, *, col, width):
        # Update the Widths
        widths = list(self._column_widths.values())
        widths.insert(col - 1, width)
        self._column_widths = dict(enumerate(widths, start=1))

        # Shift the Columns
        self._widgets.insert(col - 1, self.get_empty_column())



class InputBox(FloatingWidget):
    def __init__(self, *, label=None, pos_x, pos_y, width=15):
        super().__init__(label=label, pos_x=pos_x, pos_y=pos_y, widget_type=WidgetType.INPUT_BOX)
        self.input_confirm_callback = None
        self._width = width

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width
        if self.canvas:
            self.canvas_widget.configure(width=self.width)

    def add_callback(self, *, input_confirm_callback):
        self.input_confirm_callback = input_confirm_callback

    def handle_text_input(self, event):  # pylint: disable=unused-argument
        text = self.canvas_widget.get()
        self.input_confirm_callback(widget=self, text=text)

    def draw(self):
        if self.canvas:
            def validate_length(text):
                if text and len(text) > self.width:
                    return False
                return True
            validation = self.canvas.register(validate_length)

            self.canvas_widget = tk.Entry(self.canvas, width=self.width,
                                          validate='all', validatecommand=(validation, '%P'))

            self.canvas_widget.bind('<Return>', self.handle_text_input)

            self.redraw_widget()
