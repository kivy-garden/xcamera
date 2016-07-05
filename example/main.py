import datetime
from kivy.lang import Builder
from kivy.app import App

kv = """
#:import XCamera kivy.garden.xcamera.XCamera

BoxLayout:
    orientation: 'vertical'

    XCamera:
        id: xcamera

    BoxLayout:
        orientation: 'horizontal'
        size_hint: 1, None
        height: sp(50)

        Button:
            text: 'Set landscape'
            on_release: xcamera.set_orientation()

        Button:
            text: 'Restore orientation'
            on_release: xcamera.restore_orientation()
"""


class CameraApp(App):
    def build(self):
        return Builder.load_string(kv)


if __name__ == '__main__':
    CameraApp().run()
