import os
from unittest import mock

from kivy_garden.xcamera import platform_api, xcamera


def get_camera_class():
    """
    Continuous integration providers don't have a camera available.
    """
    if os.environ.get('CI', False):
        Camera = None
    else:
        from kivy.core.camera import Camera
    return Camera


def get_xcamera():
    """
    Helper function to return a (potentially patched) XCamera instance.
    """
    Camera = get_camera_class()
    # overrides to `None` as initializing it twice seems to freeze tests
    Camera = None
    # uses the `wraps` parameter to conditionally enable/disable mock
    with mock.patch('kivy.uix.camera.CoreCamera', wraps=Camera):
        camera = xcamera.XCamera()
    return camera


class TestBase:

    def test_darker(self):
        red = 0.1
        green = 0.2
        blue = 0.3
        alpha = 0.4
        color = (red, green, blue, alpha)
        new_color = xcamera.darker(color)
        assert new_color == (0.05, 0.1, 0.15, 0.4)

    def test_getfilename(self):
        assert xcamera.get_filename().endswith('.jpg')


class TestXCamera:

    def test_shoot(self):
        camera = get_xcamera()
        with mock.patch(
                'kivy_garden.xcamera.xcamera.take_picture') as m_take_picture:
            camera.shoot()
        assert m_take_picture.mock_calls == [
            mock.call(camera, mock.ANY, mock.ANY)]

    def test_force_landscape(self):
        camera = get_xcamera()
        assert camera._previous_orientation is None
        camera.force_landscape()
        assert camera._previous_orientation == platform_api.LANDSCAPE

    def test_restore_orientation(self):
        camera = get_xcamera()
        assert camera._previous_orientation is None
        camera.restore_orientation()
        assert camera._previous_orientation is None
        camera.force_landscape()
        assert camera._previous_orientation == platform_api.LANDSCAPE
        camera.restore_orientation()
        assert camera._previous_orientation == platform_api.LANDSCAPE
