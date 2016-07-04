import os
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.resources import resource_add_path

ROOT = os.path.dirname(os.path.abspath(__file__))
resource_add_path(ROOT)

kv = """
<XCamera>:
    # \ue800 corresponds to the camera icon in the font
    icon: u"[font=data/xcamera/icons.ttf]\ue800[/font]"
    icon_color: (0.13, 0.58, 0.95, 0.8)
    icon_size: dp(50)

    Camera:
        id: corecam
        resolution: 640, 480
        play: True
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

"""
Builder.load_string(kv)


class XCamera(FloatLayout):

    def shoot(self):
        print 'shoot'


