import datetime
from kivy.garden.xcamera import XCamera
from kivy.app import App

class CameraApp(App):
    def build(self):
        return XCamera()


if __name__ == '__main__':
    CameraApp().run()
