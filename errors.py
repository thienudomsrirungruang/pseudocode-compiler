class NotPrimitiveError(Exception):
    def __init__(self, message):
        self.message = message

class ParseError(Exception):
    def __init__(self, message):
        self.message = message
