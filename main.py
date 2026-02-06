from parser import parser
from lex import lex
# from clang import run_clang_pipeline
from transpiler import traversing, include_header, closeFile
from formatting import format

f = open("input.txt", "r")
p = lex(f)
i = 0
g = open("output.cpp", 'w')
include_header()
while (i < len(p)):
    if (p[i][0].data == 'START'):
        # print(1)
        j = i
        while (j < len(p)):
            if (p[j][0].data == 'END'):
                break
            j+=1

        ast = parser(p[i:j+1])
        print("ast :", ast)
        traversing(ast)
        i = j

    if (p[i][0].data == 'FUNC_START'):
        # print(2)
        j = i
        while (j < len(p)):
            if (p[j][0].data == 'END'):
                break
            j+=1
        if (p[j+1][0].data == "ID"):
            j+=1
        print(p[i:j+1])
        ast = parser(p[i:j+1])
        print("ast :", ast)
        traversing(ast)
        i = j
    
    i+=1

closeFile()
format()
f.close()
g.close()

# f_ = open("output.cpp", 'r')
# print(f_.read())
# f_.close()
# run_clang_pipeline("output.cpp")