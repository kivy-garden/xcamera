from __future__ import absolute_import
from kivy.utils import platform

def play_shutter():
    # bah, apparently we need to delay the import of kivy.core.audio, lese
    # kivy cannot find a camera provider, at lease on linux. Maybe a
    # gstreamer/pygame issue?
    from kivy.core.audio import SoundLoader
    sound = SoundLoader.load("data/xcamera/shutter.wav")
    sound.play()


if platform == 'android':
    from .android_api import *

else:

    # generic fallback for taking pictures. Probably not the best quality,
    # they are meant mostly for testing

    def take_picture(camera_widget, filename):
        camera_widget.texture.save(filename, flipped=False)
        play_shutter()
