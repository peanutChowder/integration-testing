

class Entry(object):
    def __init__(self,n1:str, n2:str):
        self.name=n1;
        self.number=n2;
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,Name):
        self._name=Name

    @property
    def number(self):
        return self._number
    @number.setter
    def number(self,Number):
        self._number=Number

    def __eq__(self, other):
        return self._name == other._name

    def __str__(self):
        return self._name + ", " + self._number


