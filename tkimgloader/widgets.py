
import enum


@enum.unique
class WidgetCategory(enum.Enum):
    # pylint: disable=invalid-name
    CANVAS = 'Canvas'
    FLOATING = 'Floating'


@enum.unique
class WidgetType(enum.Enum):
    # pylint: disable=invalid-name
    TEXT = 'Text'


class Widget():
    def __init__(self, *, widget_id, widget_category, widget_type, pos_x, pos_y):
        # Check Input
        if not isinstance(widget_category, WidgetCategory):
            raise ValueError(F'Invalid category "{widget_category}" Passed, not of type WidgetCategory')
        # Check Input
        if not isinstance(widget_type, WidgetType):
            raise ValueError(F'Invalid category "{widget_type}" Passed, not of type WidgetCategory')

        # Set Attributes
        self.id = widget_id
        self.category = widget_category
        self.type = widget_type
        self.pos_x = pos_x
        self.pos_y = pos_y


class Text(Widget):
    pass




