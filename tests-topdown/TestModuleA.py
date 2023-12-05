import unittest
from unittest.mock import Mock, patch

from modules.ModuleA import ModuleA
from data.Entry import Entry

class TestModuleA(unittest.TestCase):
    def setUp(self) -> None:
        self.mockB = Mock()
        self.mockC = Mock()
        self.mockD = Mock()
        self.mockE = Mock()

        self.moduleA = ModuleA(
            self.mockB,
            self.mockC,
            self.mockD,
            self.mockE
        )
        self.initialData = [
            Entry("data1", "1"),
            Entry("data2", "2")
        ]
        self.moduleA._data = [
            Entry("data1", "1"),
            Entry("data2", "2")
        ]
        self.initialFile = "file.txt"
        self.moduleA._filename = "file.txt"

    def test_parse_delete_success(self):        
        returnVal = self.moduleA.parseDelete(1)

        self.mockD.deleteData.assert_called_once_with(self.initialData, 1, self.initialFile)

        self.assertEqual(returnVal, True)

    def test_parse_delete_fail(self):
        self.mockD.deleteData.return_value = None

        returnVal = self.moduleA.parseDelete(1)

        self.mockD.deleteData.assert_called_once_with(None, 1, self.initialFile)

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
        
    def test_parse_load_success(self):
        fileData = [
            Entry("data1", "2"),
            Entry("data2", "4")
        ]

        self.mockB.loadFile.return_value = fileData.copy()

        returnVal = self.moduleA.parseLoad("file.txt")

        self.mockB.loadFile.assert_called_once_with("file.txt")

        self.assertEqual(self.moduleA._data, fileData)
        self.assertEqual(returnVal, True)

    def test_parse_load_fail(self):
        self.mockB.loadFile.return_value = None

        returnVal = self.moduleA.parseLoad("file.txt")

        self.mockB.loadFile.assert_called_once_with("file.txt")

        self.assertEqual(self.moduleA._data, None)
        self.assertEqual(returnVal, False)

    def test_parse_add_success(self):
        returnData = [
            Entry("data1", "1"),
            Entry("data2", "2"),
            Entry("data3", "3")
        ]

        self.mockD.insertData.return_value = returnData.copy()

        returnVal = self.moduleA.parseAdd("data3", "3")

        self.mockD.insertData.assert_called_once_with(self.initialData, "data3", "3", self.initialFile)

        self.assertEqual(self.moduleA._data, returnData)
        self.assertEqual(returnVal, True)   

    def test_parse_add_fail(self):
        self.mockD.insertData.return_value = None

        returnVal = self.moduleA.parseAdd("data3", "3")
        self.mockD.insertData.assert_called_once_with(self.initialData, "data3", "3", self.initialFile)

        self.assertEqual(self.moduleA._data, None)
        self.assertEqual(returnVal, False) 

    def test_run_sort_success(self):
        data = [
            Entry("data1", "1"),
            Entry("data2", "2"),
            Entry("data3", "3")
        ]

        self.mockC.sortData.return_value = data.copy()

        returnVal = self.moduleA.runSort()

        self.mockC.sortData.assert_called_once_with(self.initialData)

        self.assertEqual(self.moduleA._data, data)
        self.assertEqual(returnVal, True)  

    def test_run_sort_fail(self):
        self.mockC.sortData.return_value = None

        returnVal = self.moduleA.runSort()

        self.mockC.sortData.assert_called_once_with(self.initialData)


        self.assertEqual(self.moduleA._data, None)
        self.assertEqual(returnVal, False) 

    def test_parse_update_success(self):
        finalData = [
            Entry("data1", "1"),
            Entry("data2", "2"),
            Entry("data3", "3")
        ]

        self.mockD.updateData.return_value = finalData.copy()

        returnVal = self.moduleA.parseUpdate(2, "data3", "3")

        self.mockD.updateData.assert_called_once_with(self.initialData, 2, "data3", "3", self.initialFile)

        self.assertEqual(self.moduleA._data, finalData)
        self.assertEqual(returnVal, True)

    def test_parse_update_fail(self):
        self.mockD.updateData.return_value = None

        returnVal = self.moduleA.parseUpdate(2, "data3", "3")

        self.mockD.updateData.assert_called_once_with(self.initialData, 2, "data3", "3", self.initialFile)

        self.assertEqual(self.moduleA._data, None)
        self.assertEqual(returnVal, False)

    def test_run_exit(self):
        self.moduleA.runExit()

        self.mockE.exitProgram.assert_called_once_with()

    def test_data_getter(self):
        returnVal = self.moduleA.data

        self.assertEqual(self.initialData, returnVal)

    def test_data_setter(self):
        newData = [
            Entry("data", "99")
        ] 

        self.moduleA.data = newData.copy()

        self.assertEqual(newData, self.moduleA._data)

    @patch('builtins.print')
    def test_run_no_args(self, mockPrint):
        self.moduleA.run()

        mockPrint.assert_called_with("No command passed!")

    @patch('builtins.print')
    @patch('modules.ModuleA.ModuleA.displayHelp')
    def test_run_help(self, mockDisplayHelp, mockPrint):
        self.moduleA.run('help')

        mockDisplayHelp.assert_called_once_with()
        mockDisplayHelp.side

    @patch('builtins.print')
    def test_run_load_no_args(self, mockPrint):
        # Test without args
        self.moduleA.run('load')
        mockPrint.assert_called_with('Malformed command!')

    @patch('builtins.print')
    @patch('modules.ModuleA.ModuleA.parseLoad')
    def test_run_load(self, mockParseLoad, print):
        self.moduleA.run('load', 'file.txt')

        mockParseLoad.assert_called_once_with('file.txt')

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
    @patch('modules.ModuleA.ModuleA.parseAdd')
    def test_run_add(self, mockParseAdd, mockPrint):
        self.moduleA.run('add', 'data23', '23')

        mockParseAdd.assert_called_once_with('data23', '23')

    @patch('builtins.print')
    def test_run_sort_no_data(self, mockPrint):
        self.moduleA._data = None

        self.moduleA.run('sort')

        mockPrint.assert_called_with('No file loaded!')

    @patch('builtins.print')
    @patch('modules.ModuleA.ModuleA.runSort')
    def test_run_sort(self, mockRunSort, mockPrint):
        self.moduleA.run('sort')

        mockRunSort.assert_called_once()

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
    @patch('modules.ModuleA.ModuleA.parseUpdate')
    def test_run_update(self, mockParseUpdate, mockPrint):
        self.moduleA.run('update', 3, 'data33', '33')

        mockParseUpdate.assert_called_once_with( 3, 'data33', '33')
    
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
    @patch('modules.ModuleA.ModuleA.parseDelete')
    def test_run_update(self, mockParseDelete, mockPrint):
        self.moduleA.run('delete', 3)

        mockParseDelete.assert_called_once_with(3)

    @patch('builtins.print')
    @patch('modules.ModuleA.ModuleA.runExit')
    def test_run_runexit(self, mockRunExit, mockPrint):
        self.moduleA.run('exit')

        mockRunExit.assert_called_once()

    @patch('builtins.print')
    def test_run_unknown(self, mockPrint):
        self.moduleA.run('asdfsadf')

        mockPrint.assert_called_with("Unknown command, type 'help' for command list.")

if __name__ == '__main__':
    unittest.main()
