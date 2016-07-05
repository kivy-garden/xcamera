from __future__ import absolute_import

import os
import datetime
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.resources import resource_add_path
from .platform_api import take_picture, set_orientation, LANDSCAPE

ROOT = os.path.dirname(os.path.abspath(__file__))
resource_add_path(ROOT)

kv = """
<XCamera>:
    # \ue800 corresponds to the camera icon in the font
    icon: u"[font=data/xcamera/icons.ttf]\ue800[/font]"
    icon_color: (0.13, 0.58, 0.95, 0.8)
    icon_size: dp(50)

    Camera:
        id: camera
        resolution: 640, 480
        allow_stretch: True
        size_hint: 1, 1

    # Shoot button
    Label:
        # background circle
        canvas.before:
            Color:
                rgba: root.icon_color
            Ellipse:
                pos: self.pos
                size: self.size

        # foreground camera icon
        markup: True
        text: u"[ref=x]%s[/ref]" % root.icon

        # size
        size_hint: None, None
        size: root.icon_size, root.icon_size
        font_size: root.icon_size/2

        # position
        right: root.width - dp(10)
        center_y: root.center_y

        on_ref_press: root.shoot()

"""
Builder.load_string(kv)


class XCamera(FloatLayout):
    previous_orientation = None

    def get_filename(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.jpg')

    def shoot(self):
        filename = self.get_filename()
        take_picture(self.ids.camera, filename)

    def set_orientation(self):
        self.previous_orientation = set_orientation(LANDSCAPE)

    def restore_orientation(self):
        if self.previous_orientation is not None:
            set_orientation(self.previous_orientation)
