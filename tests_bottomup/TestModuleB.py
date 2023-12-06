import unittest
from unittest.mock import Mock, MagicMock, patch, mock_open, call

from modules.ModuleB import ModuleB
from modules.ModuleF import ModuleF
from data.Entry import Entry

class TestModuleB(unittest.TestCase):
    def setUp(self) -> None:
        self.moduleF = ModuleF()
        self.moduleB = ModuleB(self.moduleF)

    @patch("builtins.print")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_file_success(self, mockOpen: MagicMock, mockPrint: MagicMock):
        expectedData = [
            Entry("data1", "3"),
            Entry("data3", "6"),
            Entry("data5", "2")
        ]
        
        mockFile = mockOpen.return_value
        mockFile.readlines.return_value = [
            " data1,3", "data3,6 ", "data5,2"
        ]

        returnVal = self.moduleB.loadFile("file.txt")

        self.assertEqual(returnVal, expectedData)

        mockPrint.assert_has_calls([
            call("1 data1, 3"),
            call("2 data3, 6"),
            call("3 data5, 2")
        ])

    @patch("builtins.print")
    @patch("builtins.open", side_effect=IOError())
    def test_IO_error(self, mockOpen: MagicMock, mockPrint: MagicMock):
        self.moduleB.loadFile("file.txt")

        mockOpen.assert_called_once_with("file.txt")
        mockPrint.assert_has_calls([
            call("Could not read file:None"),
            call("Current Data:"),
            call("----------------------------------------------------------"),
            call("----------------------------------------------------------")
        ])

    @patch("builtins.print")
    @patch("builtins.open", side_effect=IOError)
    def test_file_not_found_error(self, mockOpen, mockPrint):
        self.moduleB.loadFile("file.txt")

        mockOpen.assert_called_once()
        mockPrint.assert_has_calls([
            call("FileNotFoundError"),
            call("Current Data:"),
            call("----------------------------------------------------------"),
            call("----------------------------------------------------------")
        ])

    def test_f_getter(self):
        returnVal = self.moduleB.f

        self.assertEqual(returnVal, self.moduleF)

    def test_f_setter(self):
        self.moduleB.f = "f"

        self.assertEqual(self.moduleB._f, "f")