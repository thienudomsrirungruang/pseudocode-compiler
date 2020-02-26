from errors import *

class Type:
    pass

class ArrayType(Type):
    def __init__(self, part_type, num_dims):
        self.part_type = part_type
        self.num_dims = num_dims

class PrimitiveType(Type):
    pass

class IntegerType(PrimitiveType):
    pass

class RealType(PrimitiveType):
    pass

class StringType(PrimitiveType):
    pass

class BooleanType(PrimitiveType):
    pass

class CharType(PrimitiveType):
    pass

def get_type_string(datatype):
    datatype_instance = datatype()
    if not isinstance(datatype_instance, PrimitiveType):
        raise NotPrimitiveError("Invalid datatype for get_type_string.")
    type_string_dict = [(IntegerType, "INTEGER"),
                            (RealType, "REAL"),
                            (StringType, "STRING"),
                            (BooleanType, "BOOLEAN"),
                            (CharType, "CHAR")]
    for type_string_matcher in type_string_dict:
        if datatype == type_string_matcher[0]:
            return type_string_matcher[1]

def get_type_from_string(datatype_string):
    type_string_dict = [(IntegerType, "INTEGER"),
                            (RealType, "REAL"),
                            (StringType, "STRING"),
                            (BooleanType, "BOOLEAN"),
                            (CharType, "CHAR")]
    for type_string_matcher in type_string_dict:
        if datatype_string == type_string_matcher[1]:
            return type_string_matcher[0]
    raise ParseError(f"Invalid datatype for get_type_from_string() {datatype_string}")
