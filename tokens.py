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
        self.regex = re.compile("^(\/\/(?:.*))((?:.|\n)*)$")

class LineSep(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^(\n)((?:.|\n)*)$")

class Whitespace(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^((?: |\t))((?:.|\n)*)$")

class Plus(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^(\+)((?:.|\n)*)$")

class Minus(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^(-)((?:.|\n)*)$")

class Keyword(Token):
    def __init__(self):
        super().__init__()

class OutputKeyword(Keyword):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^(OUTPUT)((?:.|\n)*)$")

class Literal(Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^([0-9]*\.[0-9]+|[0-9]+\.[0-9]*|[0-9]+|TRUE|FALSE|\".*\"|'.')((?:.|\n)*)$")


TOKEN_LIST = [Comment, LineSep, Whitespace, OutputKeyword, Literal, Plus, Minus] # leftmost takes priority
