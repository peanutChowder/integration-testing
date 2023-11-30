from modules.ModuleF import ModuleF
from typing import List
from data.Entry import Entry
class ModuleB:
    def __init__(self, f: ModuleF):
        self._f=f

    def loadFile(self,filename:str)->List:
        data=[]
        try:
            count = 0
            with open(filename) as fp:
                Lines = fp.readlines()
                for line in Lines:
                    count += 1
                    values=line.strip().split(",")
                    if (len(values) == 2):
                        data.append(Entry(values[0], values[1]))

        except IOError as e:
            print("Could not read file:{0.filename}".format(e))
        except FileNotFoundError:
            msg = "FileNotFoundError"
            print (msg)


        self._f.displayData(data)
        return data

    @property
    def f(self):
        return self._f
    @f.setter
    def f(self,f):
        self._f=f

