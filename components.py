import re
import queue

class ParseError(Exception):
    def __init__(self, message):
        self.message = message

class Component:
    def __init__(self):
        self.components = []

    # second step: makes the class an AST node.
    # tokens is a collections.deque()
    # raises ParseError if there is an incorrect token structure
    def parse(self, tokens):
        pass

    # third step: generates python code.
    def generate_code(self, indents=0):
        pass

    def get_graph_string(self, has_next=False, line_list=None):
        if line_list is None:
            line_list = []
        output = "".join(["│  " if i else "   " for i in line_list])
        output += ("├" if has_next else "└") + "─" + str(self) + "\r\n"
        for i, component in enumerate(self.components):
            new_has_next = i+1 < len(self.components)
            new_line_list = line_list[:]
            new_line_list.append(has_next)
            output += component.get_graph_string(new_has_next, new_line_list)
        return output

    def __repr__(self):
        return f"{self.__class__.__name__}"
    
    def __str__(self):
        return f"{self.__class__.__name__}"

class Program(Component):
    def __init__(self):
        super().__init__()
    
    def parse(self, tokens):
        while len(tokens) > 0:
            statement = Statement()
            statement.parse(tokens)
            self.components.append(statement)
    
    def generate_code(self, indents=0):
        output = "    " * indents
        for component in self.components:
            output += component.generate_code(indents)
        return output

class Statement(Component):
    def __init__(self):
        super().__init__()
    
    def parse(self, tokens):
        token = tokens[0]
        if isinstance(token, Whitespace):
            tokens.popleft() # Whitespace
        next_tok = tokens[0] # OutputKeyword OR Whitespace OR LineSep
        if isinstance(next_tok, OutputKeyword):
            output_statement = OutputStatement()
            output_statement.parse(tokens)
            self.components.append(output_statement)
        elif not isinstance(next_tok, Whitespace) and not isinstance(next_tok, LineSep) and not isinstance(next_tok, Comment):
            raise ParseError("Expected OutputKeyword or Whitespace or LineSep or Comment")
        token = tokens[0]
        if isinstance(token, Whitespace):
            tokens.popleft() # Whitespace
        token = tokens[0]
        if isinstance(token, Comment):
            tokens.popleft() # Comment
        token = tokens.popleft() # LineSep
        if not isinstance(token, LineSep):
            raise ParseError("Expected LineSep")
    
    def generate_code(self, indents=0):
        output = "    " * indents
        for component in self.components:
            output += component.generate_code(indents)
        return output

class OutputStatement(Statement):
    def __init__(self):
        super().__init__()
    
    def parse(self, tokens):
        token = tokens.popleft() # OutputKeyword
        if not isinstance(token, OutputKeyword):
            raise ParseError("Expected OutputKeyword")
        token = tokens.popleft() # Whitespace
        if not isinstance(token, Whitespace):
            raise ParseError("Expected Whitespace")
        expression = Expression() # Expression
        expression.parse(tokens)
        self.components.append(expression)
    
    def generate_code(self, indents=0):
        output = "    " * indents
        output += "print("
        output += self.components[0].generate_code()
        output += ".value)\n"
        return output

class Expression(Component):
    def __init__(self):
        super().__init__()
    
    def parse(self, tokens):
        literal = Literal()
        literal.parse(tokens)
        self.components.append(literal)
    
    def generate_code(self, indents=0):
        output = self.components[0].generate_code()
        return output

class Token(Component):
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

class Keyword(Token):
    def __init__(self):
        super().__init__()

class OutputKeyword(Keyword):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^(OUTPUT)((?:.|\n)*)$")

class Literal(Component):
    def __init__(self):
        super().__init__()
    
    def parse(self, tokens):
        token = tokens.popleft() # IntegerLiteral
        if not isinstance(token, IntegerLiteral):
            raise ParseError("Expected integer literal")
        self.components.append(token)
    
    def generate_code(self, indents=0):
        output = self.components[0].generate_code()
        return output

class IntegerLiteral(Literal, Token):
    def __init__(self):
        super().__init__()
        self.regex = re.compile("^((?:\+|-)?[0-9]+)((?:.|\n)*)$")
    
    def generate_code(self, indents=0):
        output = "INTEGER("
        output += self.value
        output += ")"
        return output

TOKEN_LIST = [Comment, LineSep, Whitespace, OutputKeyword, IntegerLiteral] # leftmost takes priority
