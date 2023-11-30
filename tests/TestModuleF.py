import unittest
from unittest.mock import patch, call
from unittest.mock import MagicMock

from modules.ModuleF import ModuleF
from data.Entry import Entry

class TestModuleF(unittest.TestCase):
    def setUp(self) -> None:
        self.moduleF = ModuleF()
        self.dummyData = [
            Entry("dummyData1", "1"),
            Entry("dummyData2", "2")
        ]

    @patch("builtins.print")
    def test_data_displayed_successfully(self, mockPrint: MagicMock):
        self.moduleF.displayData(self.dummyData)

        # mockPrint.assert_called_with("Current Data:")
        # mockPrint.assert_called_with("----------------------------------------------------------")
        mockPrint.assert_has_calls([
            call("Current Data:"),
            call("----------------------------------------------------------"),
            call("1 dummyData1, 1"),
            call("2 dummyData2, 2"),
            call("----------------------------------------------------------")
        ])

