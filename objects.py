from components import *
from tokens import *

class VariableScope():
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}
    
    def get_all_scope_variables(self):
        if self.parent is None:
            return self.variables
        return {**self.variables, **self.parent.get_all_scope_variables()}

    def add(self, variable):
        self.variables[variable.identifier] = variable

    def exists(self, identifier):
        print(f"exists({identifier}, {self.get_all_scope_variables().keys()})")
        return identifier in self.get_all_scope_variables().keys()
    
    def get(self, identifier):
        if self.exists(identifier):
            return self.get_all_scope_variables()[identifier]
        else:
            return None

    def __repr__(self):
        return f"VariableScope {self.variables}"

class Variable():
    def __init__(self, identifier, datatype):
        self.identifier = identifier
        self.datatype = datatype
        self.assigned = False
    
    def __repr__(self):
        return f"{self.identifier} : {self.datatype}{'' if self.assigned else '!'}"
