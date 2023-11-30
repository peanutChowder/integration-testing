import unittest
from unittest.mock import Mock

from modules.ModuleD import ModuleD
from data.Entry import Entry

class TestModuleD(unittest.TestCase):
    def setUp(self) -> None:
        self.mockF = Mock()
        self.mockG = Mock()
        self.moduleD = ModuleD(
            self.mockF,
            self.mockG
        )

    def test_insert_data(self):
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

        self.mockF.displayData.assert_called_once_with(data=dummyData)
        self.mockG.updateData.assert_called_once_with("file.txt", dummyData)

        self.assertEqual(returnVal, dummyData)

    def test_update_data(self):
        initialData = [
            Entry("data1", "1"),
            Entry("data2", "2"),
            Entry("data3", "3")
        ]

        finalData = [
            Entry("data1", "1"),
            Entry("newData", "4"),
            Entry("data3", "3")
        ]

        self.moduleD.updateData(
            initialData, 1,
            "newDataName", "2",
            "file.txt"
        )

        for i in range(len(initialData)):
            self.assertEqual(initialData[i], finalData[i])
        
        self.mockF.displayData.assert_called_once_with(finalData)

        self.mockG.assert_called_once_with("file.txt", finalData)

    def test_delete_data(self):
        initialData = [
            Entry("data1", "1"),
            Entry("data2", "2"),
            Entry("data3", "3")
        ]
        finalData = [
            Entry("data1", "1"),
            Entry("data2", "2"),
        ]

        self.moduleD.deleteData(
            initialData, 2, "file.txt"
        )

        self.assertEqual(len(initialData), len(finalData))

        for i in range(len(initialData)):
            self.assertEqual(initialData[i], finalData[i])

    def test_f_getter(self):
        returnVal = self.moduleD.f

        self.assertEqual(returnVal, self.mockF)

    def test_g_getter(self):
        returnVal = self.moduleD.g

        self.assertEqual(returnVal, self.mockG)

    def test_f_setter(self):
        self.moduleD.f = "f"

        self.assertEqual(self.moduleD._f, "f")

    def test_g_setter(self):
        self.moduleD.g = "g"

        self.assertEqual(self.moduleD.g, "g")