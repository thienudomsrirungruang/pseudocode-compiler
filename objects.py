from components import *
from tokens import *

class VariableScope():
    def __init__(self):
        self.variables = {}
    
    def add(self, variable):
        self.variables[variable.identifier] = variable

    def exists(self, identifier):
        print(f"exists({identifier}, {self.variables.keys()})")
        return identifier in self.variables.keys()

    def __repr__(self):
        return f"VariableScope {self.variables}"

class Variable():
    def __init__(self, identifier, datatype):
        self.identifier = identifier
        self.datatype = datatype
        self.assigned = False
    
    def __repr__(self):
        return f"{self.identifier} : {self.datatype}{'' if self.assigned else '!'}"
