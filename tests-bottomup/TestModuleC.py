import unittest
from unittest.mock import patch, call, MagicMock

from modules.ModuleC import ModuleC
from modules.ModuleF import ModuleF
from data.Entry import Entry

class TestModuleC(unittest.TestCase):
    def setUp(self) -> None:
        self.moduleF = ModuleF()
        self.moduleC = ModuleC(self.moduleF)
       
    @patch("builtins.print")
    def test_sort_data(self, mockPrint: MagicMock):
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

        mockPrint.assert_has_calls([
            call("1 data1, 92"),
            call("2 data2, 9"),
            call("3 data3, 3")
        ])

    def test_f_getter(self):
        returnVal = self.moduleC.f

        self.assertEqual(returnVal, self.moduleF)

    def test_f_setter(self):
        self.moduleC.f = "f"

        self.assertEqual(self.moduleC._f, "f")