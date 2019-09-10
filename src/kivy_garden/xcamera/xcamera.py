import datetime
import os

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.resources import resource_add_path
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.camera import Camera
from kivy.uix.label import Label

from .platform_api import LANDSCAPE, set_orientation, take_picture

ROOT = os.path.dirname(os.path.abspath(__file__))
resource_add_path(ROOT)


def darker(color, factor=0.5):
    r, g, b, a = color
    r *= factor
    g *= factor
    b *= factor
    return r, g, b, a


class XCameraIconButton(ButtonBehavior, Label):
    pass


class XCamera(Camera):
    directory = ObjectProperty(None)
    _previous_orientation = None
    __events__ = ('on_picture_taken',)

    def __init__(self, **kwargs):
        Builder.load_file(os.path.join(ROOT, "xcamera.kv"))
        super().__init__(**kwargs)

    def on_picture_taken(self, filename):
        """
        This event is fired every time a picture has been taken
        """

    def get_filename(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S.jpg')

    def shoot(self):
        def on_success(filename):
            self.dispatch('on_picture_taken', filename)
        filename = self.get_filename()
        if self.directory:
            filename = os.path.join(self.directory, filename)
        take_picture(self, filename, on_success)

    def force_landscape(self):
        self._previous_orientation = set_orientation(LANDSCAPE)

    def restore_orientation(self):
        if self._previous_orientation is not None:
            set_orientation(self._previous_orientation)
