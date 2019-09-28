from unittest import mock

from main import main


class TestMain:
    """
    Tests the `main` module.
    """

    def test_main(self):
        with mock.patch('kivy_garden.xcamera.main.CameraApp.run') as m_play:
            main()
        assert m_play.mock_calls == [mock.call()]
