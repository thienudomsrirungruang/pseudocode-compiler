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
    
    def check_exists(self, code):
        if re.search(self.regex, code):
            groups = re.match(self.regex, code)
            self.value = groups[1]
            return True, " " + groups[2]
        return False, None

class LogicalAnd(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*[^0-9a-zA-Z](AND)([^0-9a-zA-Z](?:.|\n)*)$")

class LogicalOr(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*[^0-9a-zA-Z](OR)([^0-9a-zA-Z](?:.|\n)*)$")

class LogicalNot(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*[^0-9a-zA-Z](NOT)([^0-9a-zA-Z](?:.|\n)*)$")

class Equal(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*(=)((?:.|\n)*)$")

class NotEqual(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*(<>)((?:.|\n)*)$")

class LessThan(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*(<)((?:.|\n)*)$")
        
class MoreThan(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*(>)((?:.|\n)*)$")

class LessThanEqual(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*(<=)((?:.|\n)*)$")

class MoreThanEqual(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*(>=)((?:.|\n)*)$")

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
        self.regex = re.compile("^\s*[^0-9a-zA-Z](MOD)([^0-9a-zA-Z](?:.|\n)*)$")

class Div(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*[^0-9a-zA-Z](DIV)([^0-9a-zA-Z](?:.|\n)*)$")

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
        self.regex = re.compile("^\s*[^0-9a-zA-Z](OUTPUT)([^0-9a-zA-Z](?:.|\n)*)$")

class Literal(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*([0-9]*\.[0-9]+|[0-9]+\.[0-9]*|[0-9]+|(?<=[^0-9a-zA-Z])TRUE(?=[^0-9a-zA-Z])|(?<=[^0-9a-zA-Z])FALSE(?=[^0-9a-zA-Z])|\".*\"|'.')((?:.|\n)*)$")

class Identifier(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^\s*[^0-9a-zA-Z]([a-zA-z][a-zA-z0-9]*)((?:.|\n)*)$")

TOKEN_LIST = [LineSep,
                Comment, OutputKeyword, Literal, 
                LogicalAnd, LogicalOr, LogicalNot, Div, Mod,
                Multiply, Divide, Plus, Minus,
                NotEqual, LessThanEqual, MoreThanEqual, LessThan, MoreThan, Equal,
                LeftBracket, RightBracket] # leftmost takes priority
