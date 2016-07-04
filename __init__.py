from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

kv = """
<XCamera>:
    icon: 'O'

    Camera:
        id: corecam
        resolution: 640, 480
        play: True
        allow_stretch: True
        size_hint: 1, 1

    Label:
        markup: True
        text: "[ref=shutter]%s[/ref]" % root.icon
        halign: "right"
        valign: "middle"
        text_size: self.size
        font_size: "80dp"
        on_ref_press: root.shoot()
"""
Builder.load_string(kv)


class XCamera(FloatLayout):

    def shoot(self):
        print 'shoot'


