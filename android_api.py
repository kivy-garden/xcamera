from __future__ import absolute_import
from jnius import autoclass, PythonJavaClass, java_method

Camera = autoclass('android.hardware.Camera')
AndroidActivityInfo = autoclass('android.content.pm.ActivityInfo')
AndroidPythonActivity = autoclass('org.renpy.android.PythonActivity')

class ShutterCallback(PythonJavaClass):
    __javainterfaces__ = ('android.hardware.Camera$ShutterCallback', )

    @java_method('()V')
    def onShutter(self):
        # apparently, it is enough to have an empty shutter callback to play
        # the standard shutter sound. If you pass None instead of shutter_cb
        # below, the standard sound doesn't play O_o
        pass


class PictureCallback(PythonJavaClass):
    __javainterfaces__ = ('android.hardware.Camera$PictureCallback', )

    def __init__(self, camera, filename):
        super(PictureCallback, self).__init__()
        self.camera = camera
        self.filename = filename

    @java_method('([BLandroid/hardware/Camera;)V')
    def onPictureTaken(self, data, camera):
        print 'onPictureTaken'
        s = data.tostring()
        with open(self.filename, 'wb') as f:
            f.write(s)
        print 'saved to', self.filename
        self.camera.startPreview()




def take_picture(camera_widget, filename):
    core_camera = camera_widget._camera
    camera = core_camera._android_camera # this is a Java android.hardware.Camera
    params = camera.getParameters()
    params.setFocusMode("continuous-picture")
    camera.setParameters(params)
    shutter_cb = ShutterCallback()
    picture_cb = PictureCallback(camera, filename)
    camera.takePicture(shutter_cb, None, picture_cb)



PORTRAIT = AndroidActivityInfo.SCREEN_ORIENTATION_PORTRAIT
LANDSCAPE = AndroidActivityInfo.SCREEN_ORIENTATION_LANDSCAPE

def set_orientation(value):
    previous = get_orientation()
    AndroidPythonActivity.mActivity.setRequestedOrientation(value)
    return previous

def get_orientation():
    return AndroidPythonActivity.mActivity.getRequestedOrientation()
