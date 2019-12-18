import re

class Token:
    def __init__(self):
        super().__init__()
        self.regex = None
        self.value = None

    def check_exists(self, code):
        if re.search(self.regex, code):
            groups = re.match(self.regex, code)
            self.value = groups[1]
            return True, groups[2]
        return False, None

    def __repr__(self):
        return f"{self.__class__.__name__} value {repr(self.value)}"

    def __str__(self):
        return f"{self.__class__.__name__} value {repr(self.value)}"

class Comment(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*(\/\/(?:.*))((?:.|\n)*)$")

class LineSep(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*(\n)((?:.|\n)*)$")

class Plus(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*(\+)((?:.|\n)*)$")

class Minus(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*(-)((?:.|\n)*)$")

class Multiply(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*(\*)((?:.|\n)*)$")

class Divide(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*(\/)((?:.|\n)*)$")

class Mod(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*( MOD )((?:.|\n)*)$")

class Div(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*( DIV )((?:.|\n)*)$")

class LeftBracket(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*(\()((?:.|\n)*)$")

class RightBracket(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*(\))((?:.|\n)*)$")

class Keyword(Token):
    def __init__(self):
        super().__init__()

class OutputKeyword(Keyword):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*(OUTPUT )((?:.|\n)*)$")

class Literal(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*([0-9]*\.[0-9]+|[0-9]+\.[0-9]*|[0-9]+|TRUE|FALSE|\".*\"|'.')((?:.|\n)*)$")


TOKEN_LIST = [Comment, LineSep, OutputKeyword, Literal, Div, Mod, Multiply, Divide, Plus, Minus, LeftBracket, RightBracket] # leftmost takes priority
