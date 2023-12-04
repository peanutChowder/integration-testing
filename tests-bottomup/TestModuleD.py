import unittest
from unittest.mock import MagicMock, patch, call, mock_open

from modules.ModuleD import ModuleD
from modules.ModuleF import ModuleF
from modules.ModuleG import ModuleG
from data.Entry import Entry

class TestModuleD(unittest.TestCase):
    def setUp(self) -> None:
        self.moduleF = ModuleF()
        self.moduleG = ModuleG()
        self.moduleD = ModuleD(
            self.moduleF,
            self.moduleG
        )

    @patch("builtins.print")
    @patch("builtins.open", new_callable=mock_open)
    def test_insert_data(self, mockOpen, mockPrint):
        dummyData = [
            Entry("data1", "1"),
            Entry("data2", "2"),
            Entry("data3", "3")
        ]
        

        returnVal = self.moduleD.insertData(
            dummyData, 
            "newData", "4",
            "file.txt"
        )

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

        self.assertEqual(returnVal, dummyData)

    # def test_update_data(self):
    #     initialData = [
    #         Entry("data1", "1"),
    #         Entry("data2", "2"),
    #         Entry("data3", "3")
    #     ]

    #     finalData = [
    #         Entry("data1", "1"),
    #         Entry("newData", "4"),
    #         Entry("data3", "3")
    #     ]

    #     self.moduleD.updateData(
    #         initialData, 1,
    #         "newDataName", "2",
    #         "file.txt"
    #     )

    #     for i in range(len(initialData)):
    #         self.assertEqual(initialData[i], finalData[i])
        
    #     self.mockF.displayData.assert_called_once_with(finalData)

    #     self.mockG.assert_called_once_with("file.txt", finalData)

    # def test_delete_data(self):
    #     initialData = [
    #         Entry("data1", "1"),
    #         Entry("data2", "2"),
    #         Entry("data3", "3")
    #     ]
    #     finalData = [
    #         Entry("data1", "1"),
    #         Entry("data2", "2"),
    #     ]

    #     self.moduleD.deleteData(
    #         initialData, 2, "file.txt"
    #     )

    #     self.assertEqual(len(initialData), len(finalData))

    #     for i in range(len(initialData)):
    #         self.assertEqual(initialData[i], finalData[i])

    # def test_f_getter(self):
    #     returnVal = self.moduleD.f

    #     self.assertEqual(returnVal, self.mockF)

    # def test_g_getter(self):
    #     returnVal = self.moduleD.g

    #     self.assertEqual(returnVal, self.mockG)

    # def test_f_setter(self):
    #     self.moduleD.f = "f"

    #     self.assertEqual(self.moduleD._f, "f")

    # def test_g_setter(self):
    #     self.moduleD.g = "g"

    #     self.assertEqual(self.moduleD.g, "g")