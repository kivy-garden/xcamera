import os
from threading import Thread
from unittest import mock

from kivy.app import App

from kivy_garden.xcamera.main import CameraApp
from main import main


def camera_release_workaround(app):
    """
    Upstream bug workaround, refs:
    https://github.com/kivy-garden/xcamera/issues/14
    """
    app.root.ids.xcamera._camera._device.release()


def get_camera_class():
    """
    Continuous integration providers don't have a camera available.
    """
    if os.environ.get('CI', False):
        Camera = None
    else:
        from kivy.core.camera import Camera
    return Camera


def patch_core_camera():
    Camera = get_camera_class()
    return mock.patch('kivy.uix.camera.CoreCamera', wraps=Camera)


class TestMain:
    """
    Tests the `main` module.
    """

    def test_main(self):
        """
        Checks the main starts the app properly.
        """
        app_thread = Thread(target=main)
        app_thread.start()
        app = App.get_running_app()
        # makes sure app thread is gracefully stopped before asserting
        app.stop()
        with patch_core_camera():
            app_thread.join()
        camera_release_workaround(app)
        assert type(app) == CameraApp
