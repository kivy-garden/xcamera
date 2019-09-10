from unittest import mock

from kivy_garden.xcamera import platform_api


class TestPlatformAPI:
    """
    Tests `platform_api` module.
    """

    def test_play_shutter(self):
        with mock.patch('kivy.core.audio.audio_sdl2.SoundSDL2.play') as m_play:
            platform_api.play_shutter()
        assert m_play.mock_calls == [mock.call()]

    def test_take_picture(self):
        m_camera_widget = mock.Mock()
        filename = 'filename.png'
        m_on_success = mock.Mock()
        with mock.patch.object(platform_api, 'play_shutter') as m_play_shutter:
            platform_api.take_picture(m_camera_widget, filename, m_on_success)
        assert m_play_shutter.mock_calls == [mock.call()]
        assert m_camera_widget.mock_calls == [
            mock.call.texture.save(filename, flipped=False)]
        assert m_on_success.mock_calls == [mock.call(filename)]

    def test_set_orientation(self):
        value = platform_api.LANDSCAPE
        assert platform_api.set_orientation(value) == platform_api.PORTRAIT
        assert platform_api.set_orientation(value) == platform_api.LANDSCAPE

    def test_get_orientation(self):
        value = platform_api.LANDSCAPE
        platform_api.set_orientation(value)
        assert platform_api.get_orientation() == value
