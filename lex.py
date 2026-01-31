import re

class Token:
    def __init__(self, data):
        self.data = data
    def data(self):
        return self.data
    value = 0
        

tokens = [
    (Token('START'),        r'khel_shuru'),
    (Token('END'),          r'khel_khatam'),
    (Token('IF'),           r'faisla'),
    (Token('ELSE'),         r'nahi_toh'),
    (Token('PRINT'),        r'elaan_karo'),
    (Token('VAR_DECL'),     r'khiladi'),
    (Token('ASSIGN'),       r'='),
    (Token('NUMBER'),       r'\d+'),
    (Token('STRING'),       r'"[^"]*"'),
    (Token('ID'),           r'[a-zA-Z_]\w*'),
    (Token('OP'),           r'=='),
    (Token('GE'),           r'>='),
    (Token('LE'),           r'<='),
    (Token('GT'),           r'>'),
    (Token('LT'),           r'<'),
    (Token('PLUS'),         r'[+]'),
    (Token('MINUS'),        r'-'),
    (Token('MULT'),         r'[*]'),
    (Token('DIV'),          r'/'),
    (Token('MOD'),          r'%'),
    (Token('SEMICOLON'),    r';'),
    (Token('CURLYL'),       r'{'),
    (Token('CURLYR'),       r'}'),
    (Token('EXPRESSION'),   r'\([^)]*\)'),
    (Token('SKIP'),         r'[ \t\n]+')  # Spaces and Newlines
]
def lex(file):
    file_code_text_lines = file.readlines()
    p = []
    for i in range(len(file_code_text_lines)):
        file_code_text_line = file_code_text_lines[i]
        pos = 0
        while pos < len(file_code_text_line):
            match = None
            for tag, pattern in tokens:
                regex = re.compile(pattern)
                match = regex.match(file_code_text_line, pos)
                if match:
                    if tag.data != 'SKIP':
                        tag.value = match.group(0)
                        p.append((tag, match.group(0)))
                    pos = match.end(0)
                    break
            if not match:
                raise SyntaxError(f"Illegal character at {pos}: {file_code_text_line[pos]}")
    return p

def interpreter(p: list[Token]):
    if (p[0].data=="START") and (p[len(p)-1].data=="END"):
        1
    else:
        print("Code ka khel-khatam ho gya... nahi chala")

if (__name__ == "__main__"):
    f = open("input.txt", "r")
    p = lex(f)
    print("[", end="")
    for i in range(len(p)):
            if (i == len(p)-1):
                print(p[i][0].data, ":", p[i][0].value, end="") 
            else:
                print(p[i][0].data, ":", p[i][0].value, end=", ")
    print("]")