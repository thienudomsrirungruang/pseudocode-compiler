import os
import collections
import sys

import components
import snippets
import tokens

class LexError(Exception):
    def __init__(self, message):
        self.message = message

def read_from_file(filename):
    with open(filename, 'rb') as f:
        return f.read().decode('utf-8')

def write_to_file(filename, contents):
    with open(filename, 'wb') as f:
        f.write(contents.encode('utf-8'))

# first step: converts pseudocode into a queue of components.Token()
# raises LexError if it cannot be tokenised.
def tokenise(code):
    token_list = collections.deque()
    while code != " ": # one space is always left as a result of the last linesep parse
        for token in tokens.TOKEN_LIST:
            t = token()
            results = t.check_exists(code)
            if results[0]:
                token_list.append(t)
                code = results[1]
                # print(f"code: {repr(code)}")
                break
        else:
            print(f"Current token list: {token_list}")
            raise LexError(f"Couldn't lex code near:\n>{code[:50] if len(code) > 50 else code}<")
    return token_list

if __name__ == '__main__':
    contents = read_from_file(os.path.abspath(os.path.join(__file__, '../input.pdc')))
    # sanitise input so there's always a newline both at the start and end
    contents = "\n" + contents + "\n"
    # Step 1: Tokenise / Lexing
    token_list = tokenise(contents)
    print("token list:\n" + "\n".join(list(map(str,token_list))))
    # Step 2: Create an AST (Abstract Syntax Tree)
    program = components.Program()
    try:
        program.parse(token_list)
    except Exception as e:
        print(f"token list: {token_list}")
        raise e
    print(program.get_graph_string())
    # Step 3: Generate code
    generated_code = program.generate_code()
    full_code = snippets.header + generated_code
    write_to_file(os.path.abspath(os.path.join(__file__, '../output.py')), full_code)
