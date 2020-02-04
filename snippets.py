header = \
"""import re
class _PrimitiveType:
    def strvalue(self):
        pass
    def copy(self):
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
    def strvalue(self):
        return str(self.value)
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
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
    def subtract(self, other):
        if isinstance(other, INTEGER):
            return INTEGER(self.value - other.value)
        elif isinstance(other, REAL):
            return REAL(self.value - other.value)
        else:
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
    def multiply(self, other):
        if isinstance(other, INTEGER):
            return INTEGER(self.value * other.value)
        elif isinstance(other, REAL):
            return REAL(self.value * other.value)
        else:
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
    def divide(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return REAL(self.value / other.value)
        else:
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
    def mod(self, other):
        if isinstance(other, INTEGER):
            return INTEGER(self.value % other.value)
        else:
            raise TypeError(f"INTEGER expected, got {type(other)} instead")
    def div(self, other):
        if isinstance(other, INTEGER):
            return INTEGER(self.value // other.value)
        else:
            raise TypeError(f"INTEGER expected, got {type(other)} instead")
    def equals(self, other):
        return BOOLEAN(self.value == other.value)
    def not_equals(self, other):
        return BOOLEAN(self.value != other.value)
    def less_than(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return BOOLEAN(self.value < other.value)
        else:
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
    def more_than(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return BOOLEAN(self.value > other.value)
        else:
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
    def less_than_equal(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return BOOLEAN(self.value <= other.value)
        else:
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
    def more_than_equal(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return BOOLEAN(self.value >= other.value)
        else:
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
class REAL(_PrimitiveType):
    def __init__(self, value):
        if isinstance(value, _PrimitiveType):
            value = value.value
        if isinstance(value, int):
            value = float(value)
        if not isinstance(value, float):
            raise TypeError(f"REAL expected, got {value} instead")
        self.value = value
    def strvalue(self):
        return str(self.value)
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
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
    def subtract(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return REAL(self.value - other.value)
        else:
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
    def multiply(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return REAL(self.value * other.value)
        else:
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
    def divide(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return REAL(self.value / other.value)
        else:
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
    def equals(self, other):
        return BOOLEAN(self.value == other.value)
    def not_equals(self, other):
        return BOOLEAN(self.value != other.value)
    def less_than(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return BOOLEAN(self.value < other.value)
        else:
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
    def more_than(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return BOOLEAN(self.value > other.value)
        else:
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
    def less_than_equal(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return BOOLEAN(self.value <= other.value)
        else:
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
    def more_than_equal(self, other):
        if isinstance(other, INTEGER) or isinstance(other, REAL):
            return BOOLEAN(self.value >= other.value)
        else:
            raise TypeError(f"INTEGER or REAL expected, got {type(other)} instead")
class STRING(_PrimitiveType):
    def __init__(self, value):
        if isinstance(value, _PrimitiveType):
            value = value.value
        if not isinstance(value, str):
            raise TypeError(f"STRING expected, got {value} instead")
        self.value = value
    def strvalue(self):
        return self.value
    def copy(self):
        return STRING(self.value)
    def concat(self, other):
        return STRING(self.value + other.value)
    def equals(self, other):
        return BOOLEAN(self.value == other.value)
    def not_equals(self, other):
        return BOOLEAN(self.value != other.value)
class CHAR(_PrimitiveType):
    def __init__(self, value):
        if isinstance(value, _PrimitiveType):
            value = value.value
        if not isinstance(value, str):
            raise TypeError(f"STRING expected, got {value} instead")
        if len(value) != 1:
            raise TypeError(f"STRING expected, got {value} instead")
        self.value = value
    def strvalue(self):
        return self.value
    def copy(self):
        return CHAR(self.value)
    def concat(self, other):
        return STRING(self.value + other.value)
    def equals(self, other):
        return BOOLEAN(self.value == other.value)
    def not_equals(self, other):
        return BOOLEAN(self.value != other.value)
class BOOLEAN(_PrimitiveType):
    def __init__(self, value):
        if isinstance(value, _PrimitiveType):
            value = value.value
        if not isinstance(value, bool):
            raise TypeError(f"BOOLEAN expected, got {value} instead")
        self.value = value
    def strvalue(self):
        return "TRUE" if self.value else "FALSE"
    def copy(self):
        return BOOLEAN(self.value)
    def logical_or(self, other):
        if isinstance(other, BOOLEAN):
            return BOOLEAN(self.value or other.value)
        else:
            raise TypeError(f"BOOLEAN expected, got {type(other)} instead")
    def logical_and(self, other):
        if isinstance(other, BOOLEAN):
            return BOOLEAN(self.value and other.value)
        else:
            raise TypeError(f"BOOLEAN expected, got {type(other)} instead")
    def logical_not(self):
        return BOOLEAN(not self.value)
    def equals(self, other):
        return BOOLEAN(self.value == other.value)
    def not_equals(self, other):
        return BOOLEAN(self.value != other.value)
def _INPUT(datatype):
    datatype_regexes = {
        "INTEGER": re.compile("^\d*$"),
        "REAL": re.compile("^\d*\.\d+|\d+\.\d*|\d+$"),
        "STRING": re.compile("^.*$"),
        "CHAR": re.compile("^.$"),
        "BOOLEAN": re.compile("TRUE|FALSE")
    }
    i = input(f"Enter {datatype}: ")
    while not re.search(datatype_regexes[datatype], i):
        i = input(f"Enter {datatype}: ")
    if datatype == "INTEGER":
        return INTEGER(int(i))
    if datatype == "REAL":
        return REAL(float(i))
    if datatype == "STRING":
        return STRING(i)
    if datatype == "CHAR":
        return CHAR(i)
    if datatype == "BOOLEAN":
        return BOOLEAN(i == "TRUE")
def _RANGE(a, b, s=None):
    if s is None: s = INTEGER(1)
    if not (isinstance(a, INTEGER) and isinstance(b, INTEGER) and isinstance(s, INTEGER)):
        raise TypeError("Expected inputs to _RANGE to be INTEGER")
    for i in range(a.value, b.value + 1, s.value):
        yield INTEGER(i)
"""

#TODO: DATE
