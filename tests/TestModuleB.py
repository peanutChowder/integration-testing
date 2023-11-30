import unittest
from unittest.mock import Mock, MagicMock, patch, mock_open

from modules.ModuleB import ModuleB
from data.Entry import Entry

class TestModuleB(unittest.TestCase):
    def setUp(self) -> None:
        self.mockF = Mock()
        self.moduleB = ModuleB(self.mockF)

    @patch("builtins.open", new_callable=mock_open)
    def test_load_file_success(self, mockOpen: MagicMock):
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

        self.mockF.displayData.assert_called_once_with(expectedData)

        for i in range(len(expectedData)):
            self.assertEqual(returnVal[i], expectedData[i])

    @patch("builtins.print")
    @patch("builtins.open", side_effect=IOError)
    def test_IO_error(self, mockOpen, mockPrint):
        self.moduleB.loadFile("file.txt")


        mockOpen.assert_called_once()
        mockPrint.assert_called_once_with("Could not read file:file.txt")

    @patch("builtins.print")
    @patch("builtins.open", side_effect=IOError)
    def test_file_not_found_error(self, mockOpen, mockPrint):
        self.moduleB.loadFile("file.txt")

        mockOpen.assert_called_once()
        mockPrint.assert_called_once_with("FileNotFoundError")

    def test_f_getter(self):
        returnVal = self.moduleB.f

        self.assertEqual(returnVal, self.mockF)

    def test_f_setter(self):
        self.moduleB.f = "f"

        self.assertEqual(self.moduleB._f, "f")