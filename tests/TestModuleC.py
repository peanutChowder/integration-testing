import unittest
from unittest.mock import Mock

from modules.ModuleC import ModuleC
from data.Entry import Entry

class TestModuleC(unittest.TestCase):
    def setUp(self) -> None:
        self.mockF = Mock()
        self.moduleC = ModuleC(self.mockF)
       
    def test_sort_data(self):
        initialData = [
            Entry("data3", "3"),
            Entry("data2", "9"),
            Entry("data1", "92")
        ]
        finalData = [
            Entry("data1", "92"),
            Entry("data2", "9"),
            Entry("data3", "3")
        ]

        self.moduleC.sortData(
            initialData
        )

        for i in range(len(initialData)):
            self.assertEqual(initialData[i], finalData[i])

        self.mockF.displayData.assert_called_once_with(finalData)

    def test_f_getter(self):
        returnVal = self.moduleC.f

        self.assertEqual(returnVal, self.mockF)

    def test_f_setter(self):
        self.moduleC.f = "f"

        self.assertEqual(self.moduleC._f, "f")