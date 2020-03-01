
import enum


@enum.unique
class WidgetCategory(enum.Enum):
    # pylint: disable=invalid-name
    CANVAS = 'Canvas'
    FLOATING = 'Floating'


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
    def __init__(self, *, widget_id, widget_category, widget_type, pos_x, pos_y):
        # Set Attributes
        self.id = widget_id
        self.widget_category = widget_category
        self.widget_type = widget_type
        self.pos_x = pos_x
        self.pos_y = pos_y

    @property
    def widget_category(self):
        return self._widget_category

    @widget_category.setter
    def widget_category(self, widget_category):
        if not isinstance(widget_category, WidgetCategory):
            raise ValueError(F'Invalid category "{widget_category}" Passed, not of type WidgetCategory')
        self._widget_category = widget_category

    @property
    def widget_type(self):
        return self._widget_type

    @widget_type.setter
    def widget_type(self, widget_type):
        if not isinstance(widget_type, WidgetType):
            raise ValueError(F'Invalid type " {widget_type}" Passed, not of type WidgetType')
        self._widget_type = widget_type

    def move_to(self, *, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def move_by(self, *, x, y):
        self.pos_x += x
        self.pos_y += y


class CanvasText(Widget):
    def __init__(self, *, text_id, pos_x, pos_y):
        super().__init__(widget_id=text_id, pos_x=pos_x, pos_y=pos_y,
                         widget_category=WidgetCategory.CANVAS, widget_type=WidgetType.TEXT)


class CanvasImageButton(Widget):
    def __init__(self, *, button_id, button_type, pos_x, pos_y):
        super().__init__(widget_id=button_id, pos_x=pos_x, pos_y=pos_y,
                         widget_category=WidgetCategory.CANVAS, widget_type=WidgetType.BUTTON)
        self.button_type = button_type

    @property
    def button_type(self):
        return self._button_type

    @button_type.setter
    def button_type(self, button_type):
        if not isinstance(button_type, ButtonType):
            raise ValueError(F'Invalid type " {button_type}" Passed, not of type ButtonType')
        self._button_type = button_type
