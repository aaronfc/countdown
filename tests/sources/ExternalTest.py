import unittest
from mock import MagicMock, patch

from countdown.sources.External import External, ExternalEvents
from countdown.sources.LoveSocket import LoveSocket


class ExternalTest(unittest.TestCase):

    def setUp(self):
        self.external = External()
        self.external.love_socket = MagicMock(spec=LoveSocket)

    def test_start_propagates_start_call(self):
        self.external.start()

        self.external.love_socket.start.assert_called()

    def test_stop_propagates_stop_call(self):
        self.external.stop()

        self.external.love_socket.stop.assert_called()

    def test_get_events_when_empty(self):
        self.external.love_socket.get_and_reset.return_value = 0

        output = self.external.get_events()

        self.assertEquals(0, len(output))

    def test_get_events_when_some_events_available(self):
        num_events = 2
        self.external.love_socket.get_and_reset.return_value = num_events

        output = self.external.get_events()

        self.assertEquals(num_events, len(output))
        self.assertEquals(output[0], ExternalEvents.NEW_HEART)
        self.assertEquals(output[1], ExternalEvents.NEW_HEART)

if __name__ == "__main__":
    unittest.main()