f = open("output.cpp", 'w')

f.write("#include<iostream>\n")
f.write("using namespace std;\n\n")

def start_function(p):
    try:
        if (p[0].data=="START"):
            return 1
    except:
        return 0

def declare_function(p: list):
    try:
        if ((p[0][0].data=="VAR_DECL") and (p[1][0][0].data=="ID") and (p[1][1][0].data in ["NUMBER","STRING"])):
            return 1
    except:
        return 0

def print_function(p: list):
    try:
        if ((p[0][0].data=="PRINT") and (p[1][0].data=="EXPRESSION")):
            return 1
    except:
        return 0

def assign_function(p:list):
    try:
        if ((p[0][0].data=="ASSIGN") and (p[1][0][0].data=="ID") and (p[1][1][0][0].data in ["PLUS","MINUS","MULT","DIV","MOD"])    and (p[1][1][1][0][0].data in ["ID","NUMBER","STRING"]) and (p[1][1][1][1][0].data in ["ID","NUMBER","STRING"])):
            return 1
    except:
        return 0

def ifelse_function(p:list):
    try:
        if ((p[0][0].data=="IF") and (p[1][0].data=="EXPRESSION")):
            return 1
    except:
        return 0

def while_function(p:list):
    try:
        if ((p[0][0].data=="WHILE") and (p[1][0].data=="EXPRESSION")):
            return 1
    except:
        return 0

def traversing(ast, c=0, k = 0):
    for i in range(len(ast)):
        if (start_function(ast[i])):
            f.write("int main(){\n")
            c+=1

        elif (declare_function(ast[i])):
            if (ast[i][1][1][0].data=="NUMBER"):
                temp = "\t"*c + f"int {ast[i][1][0][1]} = {ast[i][1][1][1]};\n" 
                f.write(temp)
            else:
                temp = "\t"*c + f"string {ast[i][1][0][1]} = {ast[i][1][1][1]};\n" 
                f.write(temp)

        elif (print_function(ast[i])):
            temp = "\t"*c+f"cout<<{ast[i][1][1]}<<endl;\n"
            f.write(temp)

        elif (assign_function(ast[i])):
            temp = "\t"*c+f"{ast[i][1][0][1]} = {ast[i][1][1][1][0][1]} {ast[i][1][1][0][1]} {ast[i][1][1][1][1][1]};\n"
            f.write(temp)

        elif (ifelse_function(ast[i])):
            temp = "\t"*c+f"if"+ast[i][1][1]+"{ \n"
            c+=1
            f.write(temp)
            traversing (ast[i][2], c, 1)
            c -=1
            f.write("\t"*c)
            f.write("\t"*(c-1)+"} \n")
            # print("LENGTH OF AST = ", len(ast[i]))
            if (len(ast[i])==4):
                f.write("\t"*c+"else { \n")
                c+=1
                traversing(ast[i][3], c, 1)
                c-=1
                f.write("\t"*c)
                f.write("\t"*(c-1)+"} \n")

        elif (while_function(ast[i])):
            temp = "\t"*c+f"while"+ast[i][1][1]+"{ \n"
            c +=1
            f.write(temp)
            traversing (ast[i][2], c, 1)
            c-=1
            f.write("\t"*(c)+"} \n")

    if (k == 0):
        f.write("return 0;\n}\n")

