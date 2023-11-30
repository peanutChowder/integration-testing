
class ModuleG:
    def updateData(self,openFile,data):
        try:
            with open(openFile, 'w') as FileWriter:
                for val in data:
                    FileWriter.write(val.name + "," + val.number+ "\n")
        except FileNotFoundError:
            msg = "Error updating DB File."
            print (msg)