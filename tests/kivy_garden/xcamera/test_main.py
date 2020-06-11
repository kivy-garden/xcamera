from threading import Thread
from time import sleep
from unittest import mock

from kivy.app import App
from kivy.clock import Clock

from kivy_garden.xcamera.main import CameraApp, main
from tests.test_main import camera_release_workaround, patch_core_camera


def patch_picture_taken():
    return mock.patch('kivy_garden.xcamera.main.CameraApp.picture_taken')


class TestMain:
    """
    Tests the `main` module.
    """

    def test_picture_taken(self):
        """
        Checks the `picture_taken()` listener gets called on the running app.
        """
        app_thread = Thread(target=main)
        app_thread.start()
        app = App.get_running_app()
        filename = mock.sentinel
        Clock.schedule_once(
            lambda dt: app.root.ids.xcamera.dispatch(
                'on_picture_taken', filename))
        with patch_picture_taken() as m_picture_taken, patch_core_camera():
            sleep(0.5)  # FIXME: nondeterministic approach
            # makes sure app thread is gracefully stopped before asserting
            app.stop()
            app_thread.join()
        camera_release_workaround(app)
        assert type(app) == CameraApp
        assert m_picture_taken.mock_calls == [
            mock.call(app.root.ids.xcamera, filename)]
