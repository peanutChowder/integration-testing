import unittest
from unittest.mock import Mock, MagicMock, patch, mock_open, call

from modules.ModuleA import ModuleA
from modules.ModuleB import ModuleB
from modules.ModuleC import ModuleC
from modules.ModuleD import ModuleD
from modules.ModuleE import ModuleE

from data.Entry import Entry

class TestModuleABCDE(unittest.TestCase):
    def setUp(self) -> None:
        self.mockF = Mock()
        self.mockG = Mock()

        self.moduleB = ModuleB(self.mockF)
        self.moduleC = ModuleC(self.mockF)
        self.moduleD = ModuleD(self.mockF, self.mockG)
        self.moduleE = ModuleE()

        self.moduleA = ModuleA(
            self.moduleB, 
            self.moduleC,
            self.moduleD,
            self.moduleE
        )

        self.moduleA._data = [
            Entry("data1", "1"),
            Entry("data2", "2")
        ]
        self.initialData = [
            Entry("data1", "1"),
            Entry("data2", "2")
        ]

        self.initialFile = "file.txt"
        self.moduleA._filename = "file.txt"

    def test_parse_delete_success(self):       
        expectedData = [
            Entry("data1", "1"),
        ] 

        returnVal = self.moduleA.parseDelete(1)

        self.mockF.displayData.assert_called_with(expectedData)
        self.mockG.updateData.assert_called_with(self.initialFile, expectedData)

        self.assertEqual(returnVal, True)

    def test_parse_delete_fail(self):
        returnVal = self.moduleA.parseDelete(0)

        self.mockF.displayData.assert_called_once_with([])
        self.mockG.updateData.assert_called_once_with(self.initialFile, [])

        self.assertEqual(returnVal, False)

    @patch("builtins.print")
    def test_display_help(self, mockPrint):
        self.moduleA.displayHelp()

        mockPrint.assert_called_once_with("Available Commands: \n" \
               +"load <filepath>\n" \
               +"add <name> <number>\n" \
               +"update <index> <name> <number>\n" \
               +"delete <index>\n" \
               +"sort\n" \
               +"exit"
            )
        
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_load_success(self, mockOpen: MagicMock):
        fileData = [
            Entry("data1", "2"),
            Entry("data2", "4")
        ]

        file = mockOpen.return_value
        file.readlines.return_value = [
            "data1,2\n",
            "data2,4\n"
        ]

        returnVal = self.moduleA.parseLoad(self.initialFile)

        self.mockF.displayData.assert_called_once_with(fileData)
        # self.mockB.loadFile.assert_called_once_with("file.txt")

        self.assertEqual(self.moduleA._data, fileData)
        self.assertEqual(returnVal, True)

    @patch("builtins.open", side_effect=IOError())
    def test_parse_load_fail(self, mockOpen):
        self.moduleA._data = []
        returnVal = self.moduleA.parseLoad("file.txt")

        mockOpen.assert_called_with("file.txt")
        self.assertEqual(returnVal, False)
        

    def test_parse_add_success(self):
        finalData = [
            Entry("data1", "1"),
            Entry("data2", "2"),
            Entry("data3", "3")
        ]

        returnVal = self.moduleA.parseAdd("data3", "3")

        self.mockF.displayData.assert_called_once_with(data=finalData)
        self.mockG.updateData.assert_called_once_with(self.initialFile, finalData)

        self.assertEqual(self.moduleA._data, finalData) 
        self.assertEqual(returnVal, True)   

    def test_parse_add_fail(self):
        self.moduleA._data = None

        returnVal = self.moduleA.parseAdd("data3", "3")

        self.assertEqual(self.moduleA._data, None)
        self.assertEqual(returnVal, False) 

    def test_run_sort_success(self):
        self.moduleA._data = [
            Entry("data3", "1"),
            Entry("data2", "2"),
            Entry("data1", "3")
        ]
        finalData = [
            Entry("data1", "3"),
            Entry("data2", "2"),
            Entry("data3", "1")
        ]

        returnVal = self.moduleA.runSort()

        self.mockF.displayData.assert_called_once_with(finalData)

        self.assertEqual(self.moduleA._data, finalData)
        self.assertEqual(returnVal, True)  

    def test_run_sort_fail(self):
        self.moduleA._data = None

        returnVal = self.moduleA.runSort()

        self.assertEquals(returnVal, False)
        self.assertEqual(self.moduleA._data, None)


    def test_parse_update_success(self):
        finalData = [
            Entry("data1", "1"),
            Entry("data2", "2"),
            Entry("data3", "3")
        ]

        returnVal = self.moduleA.parseUpdate(2, "data3", "3")

        self.mockF.displayData.assert_called_once_with(finalData)
        self.mockG.updateData.assert_called_once_with(self.initialFile, finalData)

        self.assertEqual(self.moduleA._data, finalData)
        self.assertEqual(returnVal, True)

    def test_parse_update_fail(self):
        self.moduleA._data = None

        returnVal = self.moduleA.parseUpdate(2, "data3", "3")

        self.assertEqual(self.moduleA._data, None)
        self.assertEqual(returnVal, False)

    @patch("builtins.print")
    @patch("builtins.exit")
    def test_run_exit(self, mockExit: MagicMock, mockPrint: MagicMock):
        self.moduleA.runExit()

        mockPrint.assert_called_once_with("Program Exit !")
        mockExit.assert_called_once_with()

    def test_data_getter(self):
        returnVal = self.moduleA.data

        self.assertEqual(self.initialData, returnVal)

    def test_data_setter(self):
        finalData = [Entry("data", "1")]
        self.moduleA.data = [Entry("data", "1")]

        self.assertEqual(finalData, self.moduleA._data)

    @patch('builtins.print')
    def test_run_no_args(self, mockPrint):
        self.moduleA.run()

        mockPrint.assert_called_with("No command passed!")

    @patch('builtins.print')
    def test_run_help(self, mockPrint):
        self.moduleA.run('help')

        help = [
            call("**********************************************************"),
            call("Command args :"),
            call("help"),
            call("**********************************************************"),
            call("Available Commands: \n" \
               +"load <filepath>\n" \
               +"add <name> <number>\n" \
               +"update <index> <name> <number>\n" \
               +"delete <index>\n" \
               +"sort\n" \
               +"exit")
        ]
        mockPrint.assert_has_calls(help)

    @patch('builtins.print')
    def test_run_load_no_args(self, mockPrint):
        # Test without args
        self.moduleA.run('load')
        mockPrint.assert_called_with('Malformed command!')

    @patch('builtins.print')
    @patch("builtins.open", new_callable=mock_open)
    def test_run_load(self, mockOpen, mockPrint):
        file = mockOpen.return_value
        file.readlines.return_value = [
            "data1,2\n",
            "data2,4\n"
        ]

        self.moduleA.run("load", "file.txt")

        mockOpen.assert_called_once_with("file.txt")
        # mockPrint.assert_called_once_with("Could not read file")
        self.mockF.displayData.assert_called_once_with([
            Entry("data1", "2"),
            Entry("data2", "4")
        ])

    @patch('builtins.print')
    def test_run_add_no_args(self, mockPrint):
        self.moduleA.run('add')
        mockPrint.assert_called_with('Malformed command!')

    @patch('builtins.print')
    def test_run_add_no_data(self, mockPrint):
        self.moduleA._data = None
        self.moduleA.run('add', 'data23', '23')

        mockPrint.assert_called_with("No file loaded!")

    @patch('builtins.print')
    def test_run_add(self, mockPrint):
        finalData = [
            *self.initialData,
            Entry("data23", "23")
        ]

        self.moduleA.run('add', 'data23', '23')

        self.mockF.displayData.assert_called_once_with(data=finalData)

        self.mockG.updateData(self.initialFile, finalData)

    @patch('builtins.print')
    def test_run_sort_no_data(self, mockPrint):
        self.moduleA._data = None

        self.moduleA.run('sort')

        mockPrint.assert_called_with('No file loaded!')

    @patch('builtins.print')
    def test_run_sort(self, mockPrint):
        self.moduleA._data = [
            Entry("data3", "3"),
            Entry("data1", "1")
        ]
        finalData = [
            Entry("data1", "1"),
            Entry("data3", "3")
        ]

        self.moduleA.run('sort')

        self.assertEquals(self.moduleA._data, finalData)
        self.mockF.displayData(finalData)

        

    @patch('builtins.print')
    def test_run_update_no_args(self, mockPrint):
        self.moduleA.run('update')

        mockPrint.assert_called_with("Malformed command!")

    @patch('builtins.print')
    def test_run_update_no_data(self, mockPrint):
        self.moduleA._data = None
        self.moduleA.run('update', 3, "data33", "33")

        mockPrint.assert_called_with("No file loaded!")

    @patch('builtins.print')
    def test_run_update(self, mockPrint):
        finalData = [
            Entry("data1", "1"),
            Entry("data33", "33")
        ]
        self.moduleA.run('update', 1, 'data33', '33')

        self.mockF.displayData.assert_called_once_with(finalData)
        self.mockG.updateData.assert_called_once_with(self.initialFile, finalData)
    
    @patch('builtins.print')
    def test_run_delete_no_args(self, mockPrint):
        self.moduleA.run('delete')

        mockPrint.assert_called_with('Malformed command!')

    @patch('builtins.print')
    def test_run_delete_no_data(self, mockPrint):
        self.moduleA._data = None
        self.moduleA.run('delete', 3)

        mockPrint.assert_called_with("No file loaded!")

    @patch('builtins.print')
    def test_run_update(self, mockPrint):
        finalData = [Entry("data1", "1")]

        self.moduleA.run('delete', 1)

        self.assertEquals(self.moduleA._data, finalData)
        self.mockF.displayData.assert_called_once_with(finalData)
        self.mockG.updateData.assert_called_once_with(self.initialFile, finalData)

    @patch('builtins.print')
    @patch("builtins.exit")
    def test_run_runexit(self, mockExit, mockPrint):
        self.moduleA.run('exit')

        mockPrint.assert_called_once_with("Program Exit !")
        mockExit.assert_called_once_with()

    @patch('builtins.print')
    def test_run_unknown(self, mockPrint):
        self.moduleA.run('asdfsadf')

        mockPrint.assert_called_with("Unknown command, type 'help' for command list.")

# if __name__ == '__main__':
#     unittest.main()
