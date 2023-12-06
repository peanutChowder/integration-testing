import unittest
from unittest.mock import patch, mock_open, call
from unittest.mock import MagicMock
import os

from modules.ModuleG import ModuleG
from data.Entry import Entry

class TestModuleG(unittest.TestCase):
    def setUp(self) -> None:
        self.moduleG = ModuleG()

    @patch("builtins.open", new_callable=mock_open)
    def test_data_updates_successfully(self, mockFile: MagicMock):
        dummyData = [
            Entry("dummyData1", "1"),
            Entry("dummyData2", "2")
        ]

        self.moduleG.updateData("testFile.txt", dummyData)
        
        mockFile.assert_called_once_with("testFile.txt", "w")
        
        file = mockFile()

        file.write.assert_has_calls([
            call("dummyData1,1\n"),
            call("dummyData2,2\n")
        ])

        file.__exit__.assert_called()

    @patch("builtins.open", side_effect=FileNotFoundError())
    @patch("builtins.print")
    def test_file_not_found(self, mockPrint: MagicMock, mockFile: MagicMock):
        dummyData = [
            Entry("dummyData1", "1"),
            Entry("dummyData2", "2")
        ]
        self.moduleG.updateData("nonExistant.txt", dummyData)

        mockFile.assert_called_once_with("nonExistant.txt", "w")
        mockPrint.assert_called_once_with("Error updating DB File.")
