from unittest import mock
from kivy_garden.xcamera import platform_api


class TestPlatformAPI:
    """
    Tests `platform_api` module.
    """

    def test_play_shutter(self):
        with mock.patch('kivy.core.audio.audio_sdl2.SoundSDL2.play') as m_play:
            platform_api.play_shutter()
        assert m_play.call_args_list == [mock.call()]
