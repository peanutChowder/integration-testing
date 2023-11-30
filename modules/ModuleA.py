from modules.ModuleB import ModuleB
from modules.ModuleC import ModuleC
from modules.ModuleD import ModuleD
from modules.ModuleE import ModuleE

class ModuleA:
    def __init__(self,b:ModuleB,c:ModuleC,d:ModuleD,e: ModuleE):
        self._b=b
        self._c=c
        self._d=d
        self._e=e
        self._data=None
        self._filename=None


    def parseDelete(self, index:int)->bool:
        self._data =  self._d.deleteData(self._data,index-1,  self._filename)
        if(self._data != None):
            return True
        return False

    def displayHelp(self)->bool:
        help = "Available Commands: \n" \
               +"load <filepath>\n" \
               +"add <name> <number>\n" \
               +"update <index> <name> <number>\n" \
               +"delete <index>\n" \
               +"sort\n" \
               +"exit"
        print(help)
        return True

    def parseLoad(self, filename:str)->bool:
        self._filename = filename
        self._data = self._b.loadFile(filename)
        if(self._data != None):
            return True
        return False

    def parseAdd(self, name:str,number:str)->bool:
        self._data =  self._d.insertData(self._data, name, number, self._filename)
        if(self._data != None):
            return True
        return False

    def runSort(self):
        self._data=self._c.sortData(self._data)
        if(self._data != None):
            return True
        return False



    def parseUpdate(self,index:int,name:str,number:str)->bool:
        self._data=self._d.updateData(self._data, index-2, name, number, self._filename)
        if(self._data !=  None):
            return True
        return False


    def runExit(self):
        self._e.exitProgam()

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self,data):
        self._f=data

    def run(self,*args):
        print ("**********************************************************")
        print ("Command args :")
        print(','.join(str(v) for v in args))
        print ("**********************************************************")
        if(len(args)==0):
            print("No command passed!")

        elif(args[0]=="help"):
            self.displayHelp()
        elif(args[0]=="load"):
            try:
                self.parseLoad(args[1])
            except IndexError:
                print("Malformed command!")
        elif(args[0]=="add"):
            try:
                if(self.data != None):
                    self.parseAdd(args[1], args[2])
                else:
                    print("No file loaded!")
            except IndexError:
                print("Malformed command!")
        elif(args[0]=="sort"):

            if(self.data != None):
                self.runSort()
            else:
                print("No file loaded!")

        elif(args[0]=="update"):
            try:
                if(self._data != None):
                    self.parseUpdate(args[1], args[2],args[3])
                else:
                    print("No file loaded!")
            except IndexError:
                print("Malformed command!")
        elif(args[0]=="delete"):
            try:
                if(self.data != None):
                    self.parseDelete(args[1])
                else:
                    print("No file loaded!")
            except IndexError:
                print("Malformed command!")
        elif(args[0]=="exit"):
            self.runExit()

        else:
            print("Unknown command, type 'help' for command list.")


