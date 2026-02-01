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
    (Token('PRINT'),        r'aelaan_karo'),
    (Token('VAR_DECL'),     r'khiladi'),
    (Token('ASSIGN'),       r'='),
    (Token("WHILE"),        r'khelte_raho'),
    (Token('NUMBER'),       r'\d+'),
    (Token('STRING'),       r'"[^"]*"'),
    (Token('ID'),           r'[a-zA-Z_]\w*'),
    (Token('NE'),           r'!='),
    (Token('EE'),           r'=='),
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
    (Token('OPENL'),        r'\('),
    (Token('CLOSER'),       r'\)'),
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
    open_found = 0
    i_ = []
    j_ = []
    i = 0
    while(i<len(p)):
        if (p[i][0].data == "OPENL"):
            i_.append(i)
            open_found += 1
        
        if ((open_found != 0) and (p[i][0].data == "CLOSER")):
            j_.append(i)
            open_found -= 1
            if (open_found == 0):
                p_temp = p[:i_[0]]
                t = Token("EXPRESSION")
                t.value = ""
                for _ in range(i_[0], j_[-1]+1):
                    t.value += p[_][1]
                t_ = tuple()
                p_temp.append(t_+(t, t.value))
                p_temp.extend(p[j_[-1]+1:])
            i -= (j_[-1] - i_[0]+1)
            p = p_temp
            i_ = []
            j_ = []
        i+=1

    return p

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