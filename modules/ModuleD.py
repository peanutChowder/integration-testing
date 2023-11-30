from modules.ModuleF import ModuleF
from modules.ModuleG import ModuleG
from typing import List
from data.Entry import Entry
class ModuleD:
    def __init__(self, f: ModuleF, g: ModuleG):

        self._f=f
        self._g=g

    def insertData(self,data:List,name:str,number:str,filename:str)->List:
        data.append(Entry(name, number))
        self.f.displayData(data=data)
        self.g.updateData(filename, data);
        return data


    def updateData(self,data:List,index:int,name:str,number:str,filename:str)->List:
        data[index+1]=Entry(name, number)
        self.f.displayData(data)
        self.g.updateData(filename, data);
        return data


    def deleteData(self,data:List,index:int,filename:str)->List:
        del data[index]
        self.f.displayData(data)
        self.g.updateData(filename, data)
        return data

    @property
    def f(self):
        return self._f
    @f.setter
    def f(self,f):
        self._f=f

    @property
    def g(self):
        return self._g
    @g.setter
    def g(self,g):
        self._g=g

