
class ModuleF:

    def displayData(self,data):
        print ("Current Data:")
        print ("----------------------------------------------------------")
        for i, val in enumerate(data):
            print(str(i+1)+" "+str(val))
        print ("----------------------------------------------------------")