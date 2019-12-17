header = \
"""class _PrimitiveType:
    pass

class INTEGER(_PrimitiveType):
    def __init__(self, value):
        if isinstance(value, _PrimitiveType):
            value = value.value
        if isinstance(value, float):
            if float % 1 == 0:
                value = int(value)
        if not isinstance(value, int):
            raise TypeError(f"INTEGER expected, got {value} instead")
        self.value = value
    def copy(self):
        return INTEGER(self.value)
    def negative(self):
        return INTEGER(-self.value)
    def positive(self):
        return INTEGER(self.value)
class REAL(_PrimitiveType):
    def __init__(self, value):
        if isinstance(value, _PrimitiveType):
            value = value.value
        if isinstance(value, int):
            value = float(value)
        if not isinstance(value, float):
            raise TypeError(f"REAL expected, got {value} instead")
        self.value = value
    def copy(self):
        return REAL(self.value)
    def negative(self):
        return REAL(-self.value)
    def positive(self):
        return REAL(self.value)
class STRING(_PrimitiveType):
    def __init__(self, value):
        if isinstance(value, _PrimitiveType):
            value = value.value
        if not isinstance(value, str):
            raise TypeError(f"STRING expected, got {value} instead")
        self.value = value
    def copy(self):
        return STRING(self.value)
class CHAR(_PrimitiveType):
    def __init__(self, value):
        if isinstance(value, _PrimitiveType):
            value = value.value
        if not isinstance(value, str):
            raise TypeError(f"STRING expected, got {value} instead")
        if len(value) != 1:
            raise TypeError(f"STRING expected, got {value} instead")
        self.value = value
    def copy(self):
        return CHAR(self.value)
class BOOLEAN(_PrimitiveType):
    def __init__(self, value):
        if isinstance(value, _PrimitiveType):
            value = value.value
        if not isinstance(value, bool):
            raise TypeError(f"BOOLEAN expected, got {value} instead")
        self.value = value
    def copy(self):
        return BOOLEAN(self.value)
"""

#TODO: DATE
