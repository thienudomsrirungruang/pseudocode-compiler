import re
from tokens import *

class ParseError(Exception):
    def __init__(self, message):
        self.message = message

class TypeError(Exception):
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
        self.type = None
    
    #TODO: Types
    def get_type(self):
        return self.type

    def parse(self, tokens):
        term = Term() # Term
        term.parse(tokens)
        self.components.append(term)
        next_tok = tokens[0]
        if isinstance(next_tok, Whitespace):
            token = tokens.popleft()
            next_tok = tokens[0]
        while isinstance(next_tok, Plus) or isinstance(next_tok, Minus):
            next_tok = tokens[0]
            if isinstance(next_tok, Whitespace):
                token = tokens.popleft()
            binaryop = BinaryOp() # BinaryOp
            binaryop.parse(tokens)
            self.components.append(binaryop)
            next_tok = tokens[0]
            if isinstance(next_tok, Whitespace):
                token = tokens.popleft()
            term = Term() # Term
            term.parse(tokens)
            self.components.append(term)
        # if isinstance(next_tok, Plus) or isinstance(next_tok, Minus):
        #     self.exprtype = "unary_op"
        #     uop = UnaryOp() # UnaryOp
        #     uop.parse(tokens)
        #     self.components.append(uop)
        #     expr = Expression() # Expression
        #     expr.parse(tokens)
        #     if expr.get_type() not in ("INTEGER", "REAL"):
        #         raise TypeError(f"UnaryOp expected INTEGER or REAL, got {expr.get_type()}")
        #     self.type = expr.get_type()
        #     self.components.append(expr)
        # else:
        #     self.exprtype = "literal"
        #     lit = LiteralComponent()
        #     lit.parse(tokens)
        #     self.type = lit.get_type()
        #     self.components.append(lit)
    
    def generate_code(self, indents=0):
        # TODO
        pass
        # if self.exprtype == "unary_op":
        #     output = self.components[1].generate_code()
        #     output += self.components[0].generate_code()
        # elif self.exprtype == "literal":
        #     output = self.components[0].generate_code()
        # return output

class Term(Component):
    def __init__(self):
        super().__init__()
        self.type = None
    
    def parse(self, tokens):
        factor = Factor() # Factor
        factor.parse(tokens)
        self.components.append(factor)
        next_tok = tokens[0]
        if isinstance(next_tok, Whitespace):
            token = tokens.popleft()
            next_tok = tokens[0]
        while isinstance(next_tok, Multiply) or isinstance(next_tok, Divide):
            next_tok = tokens[0]
            if isinstance(next_tok, Whitespace):
                token = tokens.popleft()
            binaryop = BinaryOp() # BinaryOp
            binaryop.parse(tokens)
            self.components.append(binaryop)
            next_tok = tokens[0]
            if isinstance(next_tok, Whitespace):
                token = tokens.popleft()
            factor = Factor() # Factor
            factor.parse(tokens)
            self.components.append(factor)

    def generate_code(self, indents=0):
        pass

class Factor(Component):
    def __init__(self):
        super().__init__()
        self.type = None
        self.exprtype = None
    
    def parse(self, tokens):
        next_tok = tokens[0]
        if isinstance(next_tok, LeftBracket):
            tokens.popleft()
            next_tok = tokens[0]
            if isinstance(next_tok, Whitespace):
                tokens.popleft()
            expr = Expression()
            expr.parse(tokens)
            next_tok = tokens[0]
            if isinstance(next_tok, Whitespace):
                tokens.popleft()
            token = tokens.popleft()
            if not isinstance(token, RightBracket):
                raise ParseError("Expected RightBracket")
            self.components.append(expr)
            self.exprtype = "bracket"
        elif isinstance(next_tok, Plus) or isinstance(next_tok, Minus):
            uop = UnaryOp() # UnaryOp
            uop.parse(tokens)
            self.components.append(uop)
            factor = Factor() # Factor
            factor.parse(tokens)
            # if factor.get_type() not in ("INTEGER", "REAL"):
            #     raise TypeError(f"UnaryOp expected INTEGER or REAL, got {factor.get_type()}")
            # self.type = factor.get_type()
            self.components.append(factor)
            self.exprtype = "unary_op"
        else:
            lit = LiteralComponent()
            lit.parse(tokens)
            self.components.append(lit)
            self.exprtype = "lit"

    def generate_code(self, indents=0):
        pass

class UnaryOp(Component):
    def __init__(self):
        super().__init__()
        self.value = ""

    def parse(self, tokens):
        token = tokens.popleft() # Plus OR Minus
        if not isinstance(token, Plus) and not isinstance(token, Minus):
            raise ParseError("Expected Plus or Minus")
        self.value = token.value
    
    def generate_code(self, indents=0):
        output = ""
        if self.value == "+":
            output += ".positive()"
        elif self.value == "-":
            output += ".negative()"
        return output

class BinaryOp(Component):
    def __init__(self):
        super().__init__()
        self.value = ""
    
    def parse(self, tokens):
        token = tokens.popleft()
        self.value = token.value
    
    def generate_code(self, indents=0):
        # Code is generated in the parent.
        pass

    def __repr__(self):
        return f"{self.__class__.__name__} value {repr(self.value)}"

    def __str__(self):
        return f"{self.__class__.__name__} value {repr(self.value)}"

class LiteralComponent(Component):
    def __init__(self):
        super().__init__()
        self.type = None
        self.value = None
    
    def get_type(self):
        type_matchers = {
            "^[0-9]+$": "INTEGER",
            "^[0-9]*\.[0-9]+|[0-9]+\.[0-9]*$": "REAL",
            "^TRUE|FALSE$": "BOOLEAN",
            "^\".*\"$": "STRING",
            "^'.'$": "CHAR"
        }
        for i, j in type_matchers.items():
            if re.search(re.compile(i), self.value):
                return j

    def parse(self, tokens):
        token = tokens.popleft()
        if not isinstance(token, Literal):
            raise ParseError(f"Expected Literal")
        self.value = token.value

    def generate_code(self, indents=0):
        output = self.get_type()
        output += "("
        output += self.value
        output += ")"
        return output

    def __repr__(self):
        return f"{self.__class__.__name__} value {repr(self.value)}"

    def __str__(self):
        return f"{self.__class__.__name__} value {repr(self.value)}"
