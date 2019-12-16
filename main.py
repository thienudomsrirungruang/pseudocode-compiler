import os
import components
import collections

class LexError(Exception):
    def __init__(self, message):
        self.message = message

def read_from_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def write_to_file(filename, contents):
    with open(filename, 'w') as f:
        f.write(contents)

# first step: converts pseudocode into a queue of components.Token()
# raises LexError if it cannot be tokenised.
def tokenise(code):
    tokens = collections.deque()
    while len(code) > 0:
        for token in components.TOKEN_LIST:
            t = token()
            results = t.check_exists(code)
            if results[0]:
                tokens.append(t)
                code = results[1]
                break
        else:
            raise LexError(f"Couldn't lex code near:\n{code[:50] if len(code) > 50 else code}")
    return tokens

if __name__ == '__main__':
    contents = read_from_file(os.path.abspath(os.path.join(__file__, '../input.pdc')))
    # sanitise input so there's always a newline
    if contents[-1] != "\n":
        contents += "\n"
    tokens = tokenise(contents)
    print(tokens)
    program = components.Program()
    program.parse(tokens)
    print(program.get_graph_string())
    # write_to_file(os.path.abspath(os.path.join(__file__, '../output.py')), contents)
