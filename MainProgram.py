
from modules.ModuleA import ModuleA
from modules.ModuleB import ModuleB
from modules.ModuleC import ModuleC
from modules.ModuleD import ModuleD
from modules.ModuleE import ModuleE

from modules.ModuleF import ModuleF
from modules.ModuleG import ModuleG

def main():

    ### The main function contains examples of commands that you can run to test this program
    F= ModuleF()
    G=ModuleG()
    A=ModuleA(ModuleB(F),ModuleC(F),ModuleD(F,G), ModuleE())
    print("SimpleDB>>  ")
    print ("................Execute program command ................")
    A.run()
    print ("................Execute program command ................")
    A.run("help")
    print ("................Execute program command ................")
    A.run("load","data.txt")
    print ("................Execute program command ................")
    A.run("update",3,"James","56789")
    print ("................Execute program command ................")
    A.run( "add","Ahmed","477848")
    print ("................Execute program command ................")
    A.run( "delete",2)
    print ("................Execute program command ................")
    A.run("sort")
    print ("................Execute program command ................")
    A.run(" exit")



if __name__ == "__main__":
    main()