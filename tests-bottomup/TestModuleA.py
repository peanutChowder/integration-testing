import unittest
from unittest.mock import MagicMock, patch, call, mock_open

from modules.ModuleA import ModuleA
from modules.ModuleB import ModuleB
from modules.ModuleC import ModuleC
from modules.ModuleD import ModuleD
from modules.ModuleE import ModuleE
from modules.ModuleF import ModuleF
from modules.ModuleG import ModuleG

from data.Entry import Entry

class TestModuleA(unittest.TestCase):
    def setUp(self) -> None:
        self.moduleF = ModuleF()
        self.moduleG = ModuleG()

        self.moduleB = ModuleB(self.moduleF)
        self.moduleC = ModuleC(self.moduleF)
        self.moduleD = ModuleD(self.moduleF, self.moduleG)
        self.moduleE = ModuleE()

        self.moduleA = ModuleA(
            self.moduleB,
            self.moduleC,
            self.moduleD,
            self.moduleE
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

    @patch("builtins.print")
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_delete_success(self, mockOpen: MagicMock, mockPrint: MagicMock):
        initialData = [
            Entry("data1", "1"),
            Entry("data2", "2"),
            Entry("data3", "3")
        ]
        finalData = [
            Entry("data1", "1"),
            Entry("data3", "3"),
        ]

        self.moduleA._data = initialData
        self.moduleA._filename = self.initialFile

        returnVal = self.moduleA.parseDelete(1)

        self.assertEqual(len(initialData), len(finalData))

        for i in range(len(initialData)):
            self.assertEqual(initialData[i], finalData[i])

        mockPrint.assert_has_calls([
            call("Current Data:"),
            call("----------------------------------------------------------"),
            call("1 data1, 1"),
            call("2 data3, 3"),
            call("----------------------------------------------------------")
        ])

        file = mockOpen("file.txt", "w")

        file.write.assert_has_calls([
            call("data1,1\n"),
            call("data3,3\n"),
        ])

        self.assertEqual(returnVal, True)

    def test_parse_delete_fail(self):
        self.moduleA._data = None

        returnVal = self.moduleA.parseDelete(1)

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

    @patch("builtins.print")
    @patch("builtins.open", new_callable=mock_open)  
    def test_parse_load_success(self, mockOpen: MagicMock, mockPrint: MagicMock):
        expectedData = [
            Entry("data1", "3"),
            Entry("data3", "6"),
            Entry("data5", "2")
        ]
        
        mockFile = mockOpen.return_value
        mockFile.readlines.return_value = [
            " data1,3", "data3,6 ", "data5,2"
        ]

        returnVal = self.moduleA.parseLoad("file.txt")

        mockPrint.assert_has_calls([
            call("1 data1, 3"),
            call("2 data3, 6"),
            call("3 data5, 2")
        ])

        self.assertEqual(self.moduleA._data, expectedData)
        self.assertEqual(returnVal, True)

    @patch("builtins.print")
    @patch("builtins.open", side_effect=IOError())
    def test_parse_load_fail(self, mockOpen: MagicMock, mockPrint: MagicMock):
        returnVal = self.moduleA.parseLoad("file.txt")

        mockOpen.assert_called_once_with("file.txt")
        mockPrint.assert_has_calls([
            call("Could not read file:None"),
            call("Current Data:"),
            call("----------------------------------------------------------"),
            call("----------------------------------------------------------")
        ])

        self.assertEqual(returnVal, False)

    @patch("builtins.print")
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_add_success(self, mockOpen: MagicMock, mockPrint: MagicMock):
        finalData = [
            Entry("data1", "1"),
            Entry("data2", "2"),
            Entry("data3", "3"),
            Entry("newData", "4")
        ]
        self.moduleA._data = [
            Entry("data1", "1"),
            Entry("data2", "2"),
            Entry("data3", "3")
        ]
        

        returnVal = self.moduleA.parseAdd("newData", "4")

        
        mockPrint.assert_has_calls([
            call("Current Data:"),
            call("----------------------------------------------------------"),
            call("1 data1, 1"),
            call("2 data2, 2"),
            call("3 data3, 3"),
            call("4 newData, 4"),
            call("----------------------------------------------------------")
        ])

        mockOpen.assert_called_once_with("file.txt", "w")
        
        file = mockOpen()

        file.write.assert_has_calls([
            call("data1,1\n"),
            call("data2,2\n"),
            call("data3,3\n"),
        ])

        self.assertEqual(finalData, self.moduleA._data)
        self.assertEqual(returnVal, True)   

    def test_parse_add_fail(self):
        self.moduleA._data = None

        returnVal = self.moduleA.parseAdd("data3", "3")
        
        self.assertEqual(self.moduleA._data, None)
        self.assertEqual(returnVal, False) 

    @patch("builtins.print")
    def test_run_sort_success(self, mockPrint: MagicMock):
        self.moduleA._data = [
            Entry("data3", "3"),
            Entry("data2", "9"),
            Entry("data1", "92")
        ]
        finalData = [
            Entry("data1", "92"),
            Entry("data2", "9"),
            Entry("data3", "3")
        ]

        returnVal = self.moduleA.runSort()

        for i in range(len(self.moduleA._data)):
            self.assertEqual(self.moduleA._data[i], finalData[i])

        mockPrint.assert_has_calls([
            call("1 data1, 92"),
            call("2 data2, 9"),
            call("3 data3, 3")
        ])

        self.assertEqual(self.moduleA._data, finalData)
        self.assertEqual(returnVal, True)  

    def test_run_sort_fail(self):
        self.moduleA._data = None

        returnVal = self.moduleA.runSort()

        self.assertEqual(self.moduleA._data, None)
        self.assertEqual(returnVal, False) 


    @patch("builtins.print")
    @patch("builtins.open", new_callable=mock_open)
    def test_parse_update_success(self, mockOpen: MagicMock, mockPrint: MagicMock):
        self.moduleA._data = [
            Entry("data1", "1"),
            Entry("data2", "2"),
            Entry("data3", "3")
        ]

        finalData = [
            Entry("data1", "1"),
            Entry("newData", "4"),
            Entry("data3", "3")
        ]

        returnVal = self.moduleA.parseUpdate(1, "newData", "4")

        for i in range(len(self.moduleA._data)):
            self.assertEqual(self.moduleA._data[i], finalData[i])
        
        mockPrint.assert_has_calls([
            call("Current Data:"),
            call("----------------------------------------------------------"),
            call("1 data1, 1"),
            call("2 newData, 4"),
            call("3 data3, 3"),
            call("----------------------------------------------------------")
        ])

        file = mockOpen("file.txt", "w")

        file.write.assert_has_calls([
            call("data1,1\n"),
            call("newData,4\n"),
            call("data3,3\n")
        ])
        self.assertEqual(self.moduleA._data, finalData)
        self.assertEqual(returnVal, True)

    def test_parse_update_fail(self):
        self.moduleA._data = None

        returnVal = self.moduleA.parseUpdate(2, "data3", "3")

        self.assertEqual(self.moduleA._data, None)
        self.assertEqual(returnVal, False)

    @patch('sys.exit')
    @patch('builtins.print')
    def test_run_exit(self, mockPrint: MagicMock, mockExit: MagicMock):
        self.moduleA.runExit()

        mockPrint.assert_called_once_with("Program Exit !")
        mockExit.assert_called_once_with()

    def test_data_getter(self):
        returnVal = self.moduleA.data

        self.assertEqual(self.initialData, returnVal)

    def test_data_setter(self):
        expectedData = [
            Entry("data", "99")
        ] 

        self.moduleA.data = [
            Entry("data", "99")
        ]

        self.assertEquals(expectedData, self.moduleA._data) 

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
    @patch('builtins.open',new_callable=mock_open)
    def test_run_load(self, mockOpen, mockPrint):
        expectedData = [
            Entry("data1", "3"),
            Entry("data3", "6"),
            Entry("data5", "2")
        ]
        
        mockFile = mockOpen.return_value
        mockFile.readlines.return_value = [
            " data1,3", "data3,6 ", "data5,2"
        ]


        self.moduleA.run('load', 'file.txt')
    

        mockOpen.assert_called_once_with("file.txt")
        mockPrint.assert_has_calls([
            call("1 data1, 3"),
            call("2 data3, 6"),
            call("3 data5, 2")
        ])

        self.assertEquals(self.moduleA._data, expectedData)

    @patch('builtins.print')
    def test_run_add_no_args(self, mockPrint):
        self.moduleA.run('add')
        mockPrint.assert_called_with('Malformed command!')

    @patch('builtins.print')
    def test_run_add_no_data(self, mockPrint):
        self.moduleA._data = None
        self.moduleA.run('add', 'data23', '23')

        mockPrint.assert_called_with("No file loaded!")

    @patch("builtins.print")
    @patch("builtins.open", new_callable=mock_open)
    def test_run_add(self, mockOpen: MagicMock, mockPrint: MagicMock):
        self.moduleA._data = [
            Entry("data1", "1"),
            Entry("data2", "2"),
            Entry("data3", "3")
        ]
                
        self.moduleA.run("add", "newData", "4")

        mockPrint.assert_has_calls([
            call("Current Data:"),
            call("----------------------------------------------------------"),
            call("1 data1, 1"),
            call("2 data2, 2"),
            call("3 data3, 3"),
            call("4 newData, 4"),
            call("----------------------------------------------------------")
        ])

        mockOpen.assert_called_once_with("file.txt", "w")
        
        file = mockOpen("file.txt", "w")

        file.write.assert_has_calls([
            call("data1,1\n"),
            call("data2,2\n"),
            call("data3,3\n"),
        ])            


    @patch('builtins.print')
    def test_run_sort_no_data(self, mockPrint):
        self.moduleA._data = None

        self.moduleA.run('sort')

        mockPrint.assert_called_with('No file loaded!')

    @patch('builtins.print')
    def test_run_sort(self, mockPrint):
        self.moduleA._data = [
            Entry("data3", "3"),
            Entry("data2", "9"),
            Entry("data1", "92")
        ]
        finalData = [
            Entry("data1", "92"),
            Entry("data2", "9"),
            Entry("data3", "3")
        ]

        self.moduleA.run('sort')

        for i in range(len(self.moduleA._data)):
            self.assertEqual(self.moduleA._data[i], finalData[i])

        mockPrint.assert_has_calls([
            call("1 data1, 92"),
            call("2 data2, 9"),
            call("3 data3, 3")
        ])

    @patch('builtins.print')
    def test_run_update_no_args(self, mockPrint):
        self.moduleA.run('update')

        mockPrint.assert_called_with("Malformed command!")

    @patch('builtins.print')
    def test_run_update_no_data(self, mockPrint):
        self.moduleA._data = None
        self.moduleA.run('update', 3, "data33", "33")

        mockPrint.assert_called_with("No file loaded!")

    @patch("builtins.print")
    @patch("builtins.open", new_callable=mock_open)
    def test_run_update(self, mockOpen: MagicMock, mockPrint: MagicMock):
        self.moduleA._data = [
            Entry("data1", "1"),
            Entry("data2", "2"),
            Entry("data3", "3")
        ]

        finalData = [
            Entry("data1", "1"),
            Entry("newData", "4"),
            Entry("data3", "3")
        ]

        self.moduleA.run('update', 3, 'data33', '33')

        for i in range(len(self.moduleA._data)):
            self.assertEqual(self.moduleA._data[i], finalData[i])
        
        mockPrint.assert_has_calls([
            call("Current Data:"),
            call("----------------------------------------------------------"),
            call("1 data1, 1"),
            call("2 newData, 4"),
            call("3 data3, 3"),
            call("----------------------------------------------------------")
        ])

        file = mockOpen("file.txt", "w")

        file.write.assert_has_calls([
            call("data1,1\n"),
            call("newData,4\n"),
            call("data3,3\n")
        ])
    
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
    @patch("builtins.open", new_callable=mock_open)
    def test_run_delete(self, mockOpen, mockPrint):
        initialData = [
            Entry("data1", "1"),
            Entry("data2", "2"),
            Entry("data3", "3")
        ]
        finalData = [
            Entry("data1", "1"),
            Entry("data3", "3"),
        ]

        self.moduleA._data = initialData
        self.moduleA._filename = self.initialFile

        self.moduleA.run('delete', 1)

        self.assertEqual(len(initialData), len(finalData))

        for i in range(len(initialData)):
            self.assertEqual(initialData[i], finalData[i])

        mockPrint.assert_has_calls([
            call("Current Data:"),
            call("----------------------------------------------------------"),
            call("1 data1, 1"),
            call("2 data3, 3"),
            call("----------------------------------------------------------")
        ])

        file = mockOpen("file.txt", "w")

        file.write.assert_has_calls([
            call("data1,1\n"),
            call("data3,3\n"),
        ])

    @patch('sys.exit')
    @patch('builtins.print')
    def test_run_runexit(self, mockPrint: MagicMock, mockExit: MagicMock):
        self.moduleA.run('exit')

        
        mockPrint.assert_called_once_with("Program Exit !")
        mockExit.assert_called_once_with()

    @patch('builtins.print')
    def test_run_unknown(self, mockPrint):
        self.moduleA.run('asdfsadf')

        mockPrint.assert_called_with("Unknown command, type 'help' for command list.")

# if __name__ == '__main__':
#     unittest.main()
