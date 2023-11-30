from modules.ModuleF import ModuleF
from typing import List
class ModuleC:
    def __init__(self, f: ModuleF):
        self._f=f

    def sortData(self,data:List)->List:
        data.sort(key=lambda x: x.name)
        self._f.displayData(data)
        return data

    @property
    def f(self):
        return self._f
    @f.setter
    def f(self,f):
        self._f=f

