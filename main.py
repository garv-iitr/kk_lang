from parser import parser
from lex import lex
# from clang import run_clang_pipeline
from transpiler import traversing
from formatting import format

f = open("input.txt", "r")
p = lex(f)
ast = parser(p)
print(ast)
traversing(ast)
format()
f.close()
# f_ = open("output.cpp", 'r')
# print(f_.read())
# f_.close()
# run_clang_pipeline("output.cpp")