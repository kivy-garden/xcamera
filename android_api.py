from jnius import autoclass, PythonJavaClass, java_method

Camera = autoclass('android.hardware.Camera')
AndroidActivityInfo = autoclass('android.content.pm.ActivityInfo')
AndroidPythonActivity = autoclass('org.renpy.android.PythonActivity')

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
    callback = PictureCallback(camera, filename)
    camera.takePicture(None, None, callback)



PORTRAIT = AndroidActivityInfo.SCREEN_ORIENTATION_PORTRAIT
LANDSCAPE = AndroidActivityInfo.SCREEN_ORIENTATION_LANDSCAPE

def set_orientation(value):
    previous = get_orientation()
    AndroidPythonActivity.mActivity.setRequestedOrientation(value)
    return previous

def get_orientation():
    return AndroidPythonActivity.mActivity.getRequestedOrientation()
