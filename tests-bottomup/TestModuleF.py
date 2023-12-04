import unittest
from unittest.mock import patch, call
from unittest.mock import MagicMock

from modules.ModuleF import ModuleF

class TestModuleF(unittest.TestCase):
    def setUp(self):
        self.moduleF = ModuleF()

    @patch("builtins.print")
    def testDisplayData(self, mockPrint: MagicMock):
        self.moduleF.displayData(
            ["dummyData1", "dummyData2"]
        )
    
        mockPrint.assert_has_calls([
            call("Current Data:"),
            call("----------------------------------------------------------"),
            call("1 dummyData1"),
            call("2 dummyData2"),
            call("----------------------------------------------------------")
         ])
        
