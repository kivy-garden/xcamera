from __future__ import absolute_import

import os
import datetime
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.resources import resource_add_path
from .platform_api import take_picture, set_orientation, LANDSCAPE

ROOT = os.path.dirname(os.path.abspath(__file__))
resource_add_path(ROOT)

kv = """
<IconButton>
    icon_color: (0, 0, 0, 1)
    icon_size: dp(50)

    canvas.before:
        Color:
            rgba: self.icon_color
        Ellipse:
            pos: self.pos
            size: self.size

    size_hint: None, None
    size: self.icon_size, self.icon_size
    font_size: self.icon_size/2


<XCamera>:
    # \ue800 corresponds to the camera icon in the font
    icon: u"[font=data/xcamera/icons.ttf]\ue800[/font]"
    icon_color: (0.13, 0.58, 0.95, 0.8)
    icon_size: dp(70)

    Camera:
        id: camera
        resolution: 640, 480
        allow_stretch: True
        size_hint: 1, 1

    # Shoot button
    IconButton:
        markup: True
        text: root.icon
        icon_color: root.icon_color
        icon_size: root.icon_size
        on_release: root.shoot()

        # position
        right: root.width - dp(10)
        center_y: root.center_y
"""
Builder.load_string(kv)

class IconButton(ButtonBehavior, Label):
    pass


class XCamera(FloatLayout):
    previous_orientation = None
    __events__ = ('on_picture_taken',)

    def on_picture_taken(self, filename):
        """
        This event is fired every time a picture has been taken
        """

    def get_filename(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.jpg')

    def shoot(self):
        def on_success(filename):
            self.dispatch('on_picture_taken', filename)
        #
        filename = self.get_filename()
        take_picture(self.ids.camera, filename, on_success)

    def set_orientation(self):
        self.previous_orientation = set_orientation(LANDSCAPE)

    def restore_orientation(self):
        if self.previous_orientation is not None:
            set_orientation(self.previous_orientation)

