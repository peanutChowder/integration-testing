import unittest
from unittest.mock import patch, call
from unittest.mock import MagicMock

from modules.ModuleE import ModuleE
from data.Entry import Entry

class TestModuleE(unittest.TestCase):
    def setUp(self) -> None:
        self.moduleE = ModuleE()

    @patch('sys.exit')
    @patch('builtins.print')
    def test_program_exit_msg(self, mockPrint: MagicMock, mockExit: MagicMock):
        self.moduleE.exitProgram()

        mockPrint.assert_called_once_with("Program Exit !")
        mockExit.assert_called_once_with()