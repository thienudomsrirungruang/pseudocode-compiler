from components import *
from tokens import *

class VariableScope():
    def __init__(self):
        self.variables = []
    
    def __repr__(self):
        return f"VariableScope {self.variables}"

class Variable():
    def __init__(self, identifier, datatype):
        self.identifier = identifier
        self.datatype = datatype
        self.assigned = False
    
    def __repr__(self):
        return f"{self.identifier} : {self.datatype}{'' if self.assigned else '!'}"
