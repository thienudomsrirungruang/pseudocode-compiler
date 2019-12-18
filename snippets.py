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
    def add(self, other):
        if isinstance(other, INTEGER):
            return INTEGER(self.value + other.value)
        elif isinstance(other, REAL):
            return REAL(self.value + other.value)
        else:
            raise TypeError("INTEGER or REAL expected, got type(other) instead")
    def subtract(self, other):
        if isinstance(other, INTEGER):
            return INTEGER(self.value - other.value)
        elif isinstance(other, REAL):
            return REAL(self.value - other.value)
        else:
            raise TypeError("INTEGER or REAL expected, got type(other) instead")
    def multiply(self, other):
        if isinstance(other, INTEGER):
            return INTEGER(self.value * other.value)
        elif isinstance(other, REAL):
            return REAL(self.value * other.value)
        else:
            raise TypeError("INTEGER or REAL expected, got type(other) instead")
    def divide(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return REAL(self.value / other.value)
        else:
            raise TypeError("INTEGER or REAL expected, got type(other) instead")
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
    def add(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return REAL(self.value + other.value)
        else:
            raise TypeError("INTEGER or REAL expected, got type(other) instead")
    def subtract(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return REAL(self.value - other.value)
        else:
            raise TypeError("INTEGER or REAL expected, got type(other) instead")
    def multiply(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return REAL(self.value * other.value)
        else:
            raise TypeError("INTEGER or REAL expected, got type(other) instead")
    def divide(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return REAL(self.value / other.value)
        else:
            raise TypeError("INTEGER or REAL expected, got type(other) instead")
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
