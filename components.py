import re
from tokens import *
from objects import *

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
        scope = Scope()
        scope.parse(tokens)
        self.components.append(scope)
    
    def generate_code(self, indents=0):
        output = self.components[0].generate_code()
        return output

# TODO: Local variables / constants
# TODO: Actual scope handling
class Scope(Component):
    def __init__(self):
        super().__init__()

    def parse(self, tokens, variable_scope=None):
        if variable_scope is None:
            variable_scope = VariableScope()
        while len(tokens) > 0:
            next_tok = tokens[0]
            if isinstance(next_tok, EndifKeyword):
                break
            statement = Statement()
            statement.parse(tokens, variable_scope)
            self.components.append(statement)
        print(f'variable_scope {variable_scope}')
    
    def generate_code(self, indents=0):
        output = ""
        for component in self.components:
            output += component.generate_code(indents)
        return output

class Statement(Component):
    def __init__(self):
        super().__init__()
    
    def parse(self, tokens, variable_scope):
        token = tokens[0]
        next_tok = tokens[0] # OutputKeyword OR LineSep
        if isinstance(next_tok, OutputKeyword):
            output_statement = OutputStatement()
            output_statement.parse(tokens, variable_scope)
            self.components.append(output_statement)
        elif isinstance(next_tok, DeclareKeyword):
            declare_variable_statement = DeclareVariableStatement()
            declare_variable_statement.parse(tokens, variable_scope)
            self.components.append(declare_variable_statement)
        elif isinstance(next_tok, Identifier):
            assign_variable_statement = AssignVariableStatement()
            assign_variable_statement.parse(tokens, variable_scope)
            self.components.append(assign_variable_statement)
        elif isinstance(next_tok, IfKeyword):
            if_statement = IfStatement()
            if_statement.parse(tokens, variable_scope)
            self.components.append(if_statement)
        elif not isinstance(next_tok, LineSep) and not isinstance(next_tok, Comment):
            raise ParseError("Expected IfKeyword or OutputKeyword or DeclareKeyword or Identifier or LineSep or Comment")
        token = tokens[0]
        if isinstance(token, Comment):
            tokens.popleft() # Comment
        token = tokens.popleft() # LineSep
        if not isinstance(token, LineSep):
            raise ParseError("Expected LineSep")
    
    def generate_code(self, indents=0):
        if len(self.components) > 0:
            print(f"Statement (child: {self.components[0]}) generate_code({indents})")
            output = "    " * indents
            for component in self.components:
                output += component.generate_code(indents)
            return output
        else:
            return ''

class IfStatement(Component):
    def __init__(self):
        super().__init__()
    
    def parse(self, tokens, variable_scope):
        token = tokens.popleft() # IfKeyword
        if not isinstance(token, IfKeyword):
            raise ParseError("Expected IfKeyword")
        expression = LogicalOrExpression() # Expression
        expression.parse(tokens, variable_scope)
        if expression.get_type() != "BOOLEAN":
            raise ParseError(f"IF statement expected BOOLEAN, got {expression.get_type()} instead")
        self.components.append(expression)
        while isinstance(tokens[0], LineSep):
            tokens.popleft()
        token = tokens.popleft() # ThenKeyword
        if not isinstance(token, ThenKeyword):
            raise ParseError("Expected ThenKeyword")
        scope = Scope()
        scope.parse(tokens, variable_scope)
        self.components.append(scope)
        token = tokens.popleft() # EndifKeyword
        if not isinstance(token, EndifKeyword):
            raise ParseError("Expected EndifKeyword")
    
    def generate_code(self, indents=0):
        print(f"IfStatement generate_code({indents})")
        output = "if "
        output += self.components[0].generate_code()
        output += ":\n"
        output += self.components[1].generate_code(indents + 1)
        return output

class OutputStatement(Component):
    def __init__(self):
        super().__init__()
    
    def parse(self, tokens, variable_scope):
        token = tokens.popleft() # OutputKeyword
        if not isinstance(token, OutputKeyword):
            raise ParseError("Expected OutputKeyword")
        expression = LogicalOrExpression() # Expression
        expression.parse(tokens, variable_scope)
        self.components.append(expression)

    def generate_code(self, indents=0):
        output = "print("
        output += self.components[0].generate_code()
        output += ".value)\n"
        return output

class DeclareVariableStatement(Component):
    def __init__(self):
        super().__init__()
    
    def parse(self, tokens, variable_scope):
        token = tokens.popleft() # DeclareKeyword
        if not isinstance(token, DeclareKeyword):
            raise ParseError("Expected DeclareKeyword")
        token = tokens.popleft() # Identifier
        if not isinstance(token, Identifier):
            raise ParseError("Expected Identifier")
        identifier = token.value
        token = tokens.popleft() # Colon
        if not isinstance(token, Colon):
            raise ParseError("Expected Colon")
        token = tokens.popleft() # Datatype
        if not isinstance(token, Datatype):
            raise ParseError("Expected Datatype")
        datatype = token.value
        variable_scope.add(Variable(identifier, datatype))

    def generate_code(self, indents=0):
        return ""

class AssignVariableStatement(Component):
    def __init__(self):
        super().__init__()
        self.identifier = None
        self.variable = None
    
    def parse(self, tokens, variable_scope):
        token = tokens.popleft() # Identifier
        if not isinstance(token, Identifier):
            raise ParseError("Expected Identifier")
        self.identifier = token
        self.variable = variable_scope.get(self.identifier.value)
        token = tokens.popleft() # Arrow
        if not isinstance(token, Arrow):
            raise ParseError("Expected Arrow")
        expression = LogicalOrExpression()
        expression.parse(tokens, variable_scope)
        self.components.append(expression)
        if not variable_scope.exists(self.identifier.value):
            raise ParseError(f"Variable {self.identifier.value} referenced before declaration")
        self.variable.assigned = True
    
    def generate_code(self, indents=0):
        output = self.identifier.value
        output += "="
        output += self.variable.datatype
        output += "("
        output += self.components[0].generate_code(indents)
        output += ")\n"
        return output

class LogicalOrExpression(Component):
    def __init__(self):
        super().__init__()
        self.type = None
    
    def get_type(self):
        return self.type
    
    def parse(self, tokens, variable_scope):
        logical_and_exp = LogicalAndExpression() # LogicalAndExpression
        logical_and_exp.parse(tokens, variable_scope)
        self.components.append(logical_and_exp)
        self.type = logical_and_exp.get_type()
        next_tok = tokens[0]
        while isinstance(next_tok, LogicalOr):
            if self.type != "BOOLEAN":
                raise ParseError(f"BOOLEAN expected, got {self.type} instead")
            binaryop = BinaryOp() # BinaryOp
            binaryop.parse(tokens, variable_scope)
            self.components.append(binaryop)
            logical_and_exp = LogicalAndExpression() # LogicalAndExpression
            logical_and_exp.parse(tokens, variable_scope)
            self.components.append(logical_and_exp)
            if logical_and_exp.get_type() != "BOOLEAN":
                raise ParseError(f"BOOLEAN expected, got {self.type} instead")
            next_tok = tokens[0]
    
    def generate_code(self, indents=0):
        output = ""
        output += self.components[0].generate_code()
        for i in range(1, len(self.components), 2):
            if self.components[i].value == "OR": # BinaryOp
                output += ".logical_or("
                output += self.components[i+1].generate_code()
                output += ")"
        return output

    def __repr__(self):
        return f"{self.__class__.__name__} type {self.get_type()}"

    def __str__(self):
        return f"{self.__class__.__name__} type {self.get_type()}"

class LogicalAndExpression(Component):
    def __init__(self):
        super().__init__()
        self.type = None
    
    def get_type(self):
        return self.type
    
    def parse(self, tokens, variable_scope):
        equality_exp = EqualityExpression() # EqualityExpression
        equality_exp.parse(tokens, variable_scope)
        self.components.append(equality_exp)
        self.type = equality_exp.get_type()
        next_tok = tokens[0]
        while isinstance(next_tok, LogicalAnd):
            if self.type != "BOOLEAN":
                raise ParseError(f"BOOLEAN expected, got {self.type} instead")
            binaryop = BinaryOp() # BinaryOp
            binaryop.parse(tokens, variable_scope)
            self.components.append(binaryop)
            equality_exp = EqualityExpression() # EqualityExp
            equality_exp.parse(tokens, variable_scope)
            self.components.append(equality_exp)
            if equality_exp.get_type() != "BOOLEAN":
                raise ParseError(f"BOOLEAN expected, got {self.type} instead")
            next_tok = tokens[0]
    
    def generate_code(self, indents=0):
        output = ""
        output += self.components[0].generate_code()
        for i in range(1, len(self.components), 2):
            if self.components[i].value == "AND": # BinaryOp
                output += ".logical_and("
                output += self.components[i+1].generate_code()
                output += ")"
        return output

    def __repr__(self):
        return f"{self.__class__.__name__} type {self.get_type()}"

    def __str__(self):
        return f"{self.__class__.__name__} type {self.get_type()}"

class EqualityExpression(Component):
    def __init__(self):
        super().__init__()
        self.type = None
    
    def get_type(self):
        return self.type
    
    def parse(self, tokens, variable_scope):
        relational_exp = RelationalExpression() # RelationalExpression
        relational_exp.parse(tokens, variable_scope)
        self.components.append(relational_exp)
        self.type = relational_exp.get_type()
        next_tok = tokens[0]
        while isinstance(next_tok, Equal) or isinstance(next_tok, NotEqual):
            self.type = "BOOLEAN"
            binaryop = BinaryOp() # BinaryOp
            binaryop.parse(tokens, variable_scope)
            self.components.append(binaryop)
            relational_exp = RelationalExpression() # RelationalExpression
            relational_exp.parse(tokens, variable_scope)
            self.components.append(relational_exp)
            next_tok = tokens[0]
    
    def generate_code(self, indents=0):
        output = ""
        output += self.components[0].generate_code()
        for i in range(1, len(self.components), 2):
            if self.components[i].value == "=": # BinaryOp
                output += ".equals("
                output += self.components[i+1].generate_code()
                output += ")"
            elif self.components[i].value == "<>": # BinaryOp
                output += ".not_equals("
                output += self.components[i+1].generate_code()
                output += ")"
        return output

    def __repr__(self):
        return f"{self.__class__.__name__} type {self.get_type()}"

    def __str__(self):
        return f"{self.__class__.__name__} type {self.get_type()}"

class RelationalExpression(Component):
    def __init__(self):
        super().__init__()
        self.type = None
    
    def get_type(self):
        return self.type
    
    def parse(self, tokens, variable_scope):
        additive_exp = AdditiveExpression() # AdditiveExpression
        additive_exp.parse(tokens, variable_scope)
        self.components.append(additive_exp)
        self.type = additive_exp.get_type()
        next_tok = tokens[0]
        if isinstance(next_tok, LessThanEqual) or isinstance(next_tok, MoreThanEqual) or isinstance(next_tok, MoreThan) or isinstance(next_tok, LessThan):
            if self.type not in ("INTEGER", "REAL"):
                raise ParseError(f"INTEGER or REAL expected, got {self.type} instead")
            self.type = "BOOLEAN"
        while isinstance(next_tok, LessThanEqual) or isinstance(next_tok, MoreThanEqual) or isinstance(next_tok, MoreThan) or isinstance(next_tok, LessThan):
            binaryop = BinaryOp() # BinaryOp
            binaryop.parse(tokens, variable_scope)
            self.components.append(binaryop)
            additive_exp = AdditiveExpression() # AdditiveExpression
            additive_exp.parse(tokens, variable_scope)
            self.components.append(additive_exp)
            if additive_exp.get_type() not in ("INTEGER", "REAL"):
                raise ParseError(f"INTEGER or REAL expected, got {self.type} instead")
            next_tok = tokens[0]
    
    def generate_code(self, indents=0):
        output = ""
        output += self.components[0].generate_code()
        for i in range(1, len(self.components), 2):
            if self.components[i].value == "<=": # BinaryOp
                output += ".less_than_equal("
                output += self.components[i+1].generate_code()
                output += ")"
            if self.components[i].value == "<": # BinaryOp
                output += ".less_than("
                output += self.components[i+1].generate_code()
                output += ")"
            if self.components[i].value == ">=": # BinaryOp
                output += ".more_than_equal("
                output += self.components[i+1].generate_code()
                output += ")"
            if self.components[i].value == ">": # BinaryOp
                output += ".more_than("
                output += self.components[i+1].generate_code()
                output += ")"
        return output

    def __repr__(self):
        return f"{self.__class__.__name__} type {self.get_type()}"

    def __str__(self):
        return f"{self.__class__.__name__} type {self.get_type()}"

class AdditiveExpression(Component):
    def __init__(self):
        super().__init__()
        self.type = None

    def get_type(self):
        return self.type

    def parse(self, tokens, variable_scope):
        term = Term() # Term
        term.parse(tokens, variable_scope)
        self.components.append(term)
        self.type = term.get_type()
        next_tok = tokens[0]
        while isinstance(next_tok, Plus) or isinstance(next_tok, Minus):
            if self.type not in ("INTEGER", "REAL"):
                raise ParseError(f"INTEGER or REAL expected, got {self.type} instead")
            binaryop = BinaryOp() # BinaryOp
            binaryop.parse(tokens, variable_scope)
            self.components.append(binaryop)
            term = Term() # Term
            term.parse(tokens, variable_scope)
            self.components.append(term)
            if term.get_type() not in ("INTEGER", "REAL"):
                raise ParseError(f"INTEGER or REAL expected, got {term.type} instead")
            if term.get_type() == "REAL":
                self.type = "REAL"
            next_tok = tokens[0]
    
    def generate_code(self, indents=0):
        output = ""
        output += self.components[0].generate_code()
        for i in range(1, len(self.components), 2):
            if self.components[i].value == "+": # BinaryOp
                output += ".add("
                output += self.components[i+1].generate_code()
                output += ")"
            elif self.components[i].value == "-": # BinaryOp
                output += ".subtract("
                output += self.components[i+1].generate_code()
                output += ")"
        return output

    def __repr__(self):
        return f"{self.__class__.__name__} type {self.get_type()}"

    def __str__(self):
        return f"{self.__class__.__name__} type {self.get_type()}"

class Term(Component):
    def __init__(self):
        super().__init__()
        self.type = None
    
    def get_type(self):
        return self.type

    def parse(self, tokens, variable_scope):
        factor = Factor() # Factor
        factor.parse(tokens, variable_scope)
        self.components.append(factor)
        self.type = factor.get_type()
        next_tok = tokens[0]
        while isinstance(next_tok, Multiply) or isinstance(next_tok, Divide) or isinstance(next_tok, Div) or isinstance(next_tok, Mod):
            if isinstance(next_tok, Multiply) or isinstance(next_tok, Divide):
                if self.type not in ("INTEGER", "REAL"):
                    raise ParseError(f"INTEGER or REAL expected, got {self.type} instead")
            else:
                if self.type not in ("INTEGER"):
                    raise ParseError(f"INTEGER or REAL expected, got {self.type} instead")
            binaryop = BinaryOp() # BinaryOp
            binaryop.parse(tokens, variable_scope)
            if binaryop.value == "/":
                self.type == "REAL"
            self.components.append(binaryop)
            factor = Factor() # Factor
            factor.parse(tokens, variable_scope)
            self.components.append(factor)
            if binaryop.value in ("/", "*"):
                if factor.get_type() not in ("INTEGER", "REAL"):
                    raise ParseError(f"INTEGER or REAL expected, got {factor.type} instead")
                if factor.type == "REAL":
                    self.type = "REAL"
            else:
                if factor.get_type() != "INTEGER":
                    raise ParseError(f"INTEGER expected, got {factor.type} instead")
            next_tok = tokens[0]

    def generate_code(self, indents=0):
        output = ""
        output += self.components[0].generate_code()
        for i in range(1, len(self.components), 2):
            if self.components[i].value == "*": # BinaryOp
                output += ".multiply("
                output += self.components[i+1].generate_code()
                output += ")"
            elif self.components[i].value == "/":
                output += ".divide("
                output += self.components[i+1].generate_code()
                output += ")"
            elif self.components[i].value == "DIV":
                output += ".div("
                output += self.components[i+1].generate_code()
                output += ")"
            elif self.components[i].value == "MOD":
                output += ".mod("
                output += self.components[i+1].generate_code()
                output += ")"
        return output
    
    def __repr__(self):
        return f"{self.__class__.__name__} type {self.get_type()}"

    def __str__(self):
        return f"{self.__class__.__name__} type {self.get_type()}"

class Factor(Component):
    def __init__(self):
        super().__init__()
        self.type = None
        self.exprtype = None
    
    def get_type(self):
        return self.type

    def parse(self, tokens, variable_scope):
        next_tok = tokens[0]
        if isinstance(next_tok, LeftBracket):
            tokens.popleft()
            expr = LogicalOrExpression()
            expr.parse(tokens, variable_scope)
            token = tokens.popleft()
            if not isinstance(token, RightBracket):
                raise ParseError("Expected RightBracket")
            self.components.append(expr)
            self.exprtype = "bracket"
            self.type = expr.get_type()
        elif isinstance(next_tok, Plus) or isinstance(next_tok, Minus) or isinstance(next_tok, LogicalNot):
            uop = UnaryOp() # UnaryOp
            uop.parse(tokens, variable_scope)
            self.components.append(uop)
            factor = Factor() # Factor
            factor.parse(tokens, variable_scope)
            self.components.append(factor)
            self.exprtype = "unary_op"
            self.type = factor.get_type()
            if isinstance(next_tok, Plus) or isinstance(next_tok, Minus):
                if self.type not in ("INTEGER", "REAL"):
                    raise ParseError(f"Expected INTEGER or REAL, got {self.type} instead")
            elif isinstance(next_tok, LogicalNot):
                if self.type not in ("BOOLEAN"):
                    raise ParseError(f"Expected BOOLEAN, got {self.type} instead")
        elif isinstance(next_tok, Identifier):
            self.exprtype = "identifier"
            token = tokens.popleft() # Identifier
            self.identifier = token.value
            if not variable_scope.exists(self.identifier):
                raise ParseError(f"Variable {self.identifier} referenced before declaration")
            self.variable = variable_scope.get(self.identifier)
            if not self.variable.assigned:
                raise ParseError(f"Variable {self.identifier} referenced before assignment")
            self.type = self.variable.datatype
        else:
            lit = LiteralComponent()
            lit.parse(tokens, variable_scope)
            self.components.append(lit)
            self.exprtype = "lit"
            self.type = lit.get_type()

    def generate_code(self, indents=0):
        if self.exprtype == "bracket":
            output = self.components[0].generate_code()
            return output
        elif self.exprtype == "unary_op":
            output = self.components[1].generate_code()
            output += self.components[0].generate_code()
            return output
        elif self.exprtype == "lit":
            output = self.components[0].generate_code()
            return output
        elif self.exprtype == "identifier":
            output = self.identifier
            return output
    
    def __repr__(self):
        return f"{self.__class__.__name__} type {self.get_type()} exprtype {self.exprtype}"

    def __str__(self):
        return f"{self.__class__.__name__} type {self.get_type()} exprtype {self.exprtype}"

class UnaryOp(Component):
    def __init__(self):
        super().__init__()
        self.value = ""

    def parse(self, tokens, variable_scope):
        token = tokens.popleft() # Plus OR Minus
        if not isinstance(token, Plus) and not isinstance(token, Minus) and not isinstance(token, LogicalNot):
            raise ParseError("Expected Plus or Minus or LogicalNot")
        self.value = token.value
    
    def generate_code(self, indents=0):
        output = ""
        if self.value == "+":
            output += ".positive()"
        elif self.value == "-":
            output += ".negative()"
        elif self.value == "NOT":
            output += ".logical_not()"
        return output

    def __repr__(self):
        return f"{self.__class__.__name__} value {repr(self.value)}"

    def __str__(self):
        return f"{self.__class__.__name__} value {repr(self.value)}"

#TODO: string concat &
class BinaryOp(Component):
    def __init__(self):
        super().__init__()
        self.value = ""
    
    def parse(self, tokens, variable_scope):
        token = tokens.popleft()
        self.value = token.value
    
    def generate_code(self, indents=0):
        # Code is generated in the parent.
        pass

    def __repr__(self):
        return f"{self.__class__.__name__} value {repr(self.value)}"

    def __str__(self):
        return f"{self.__class__.__name__} value {repr(self.value)}"

#TODO: string escaped literals
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
            "^\"[^\n\"]*\"$": "STRING",
            "^'.'$": "CHAR"
        }
        for i, j in type_matchers.items():
            if re.search(re.compile(i), self.value):
                return j

    def parse(self, tokens, variable_scope):
        token = tokens.popleft()
        if not isinstance(token, Literal):
            raise ParseError(f"Expected Literal")
        self.value = token.value

    def generate_code(self, indents=0):
        if self.get_type() not in ("BOOLEAN", "DATE"):
            output = self.get_type()
            output += "("
            output += self.value
            output += ")"
            return output
        elif self.get_type() == "BOOLEAN":
            output = "BOOLEAN("
            output += "True" if self.value == "TRUE" else "False"
            output += ")"
            return output
        else:
            return ""

    def __repr__(self):
        return f"{self.__class__.__name__} value {repr(self.value)} type {self.get_type()}"

    def __str__(self):
        return f"{self.__class__.__name__} value {repr(self.value)} type {self.get_type()}"
