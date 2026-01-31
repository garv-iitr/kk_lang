with open("output.cpp", "w") as f:

    f.write("#include<iostream>\n")
    f.write("using namespace std;")

    def start_function(p):
        if (p[0].data=="START"):
            return 1
        return 0
    
    def declare_function(p: list):
        if ((p[0][0].data=="VAR_DECL") and (p[1][0][0].data=="ID") and (p[1][1][0].data in ["NUMBER","STRING"])):
            return 1
        return 0
    
    def print_function(p: list):
        if ((p[0][0].data=="PRINT") and (p[1][0].data=="EXPRESSION")):
            return 1
        return 0
    
    def assign_function(p:list):
        if ((p[0][0].data=="ASSIGN") and (p[1][0][0].data=="ID") and (p[1][1][0][0].data in ["PLUS","MINUS","MULT","DIV","MOD"]) and (p[1][1][1][0][0].data in ["ID","NUMBER","STRING"]) and (p[1][1][1][1][0].data in ["ID","NUMBER","STRING"])):
            return 1
        return 0
    
    def ifelse_function(p:list):
        if ((p[0][0].data=="IF") and (p[1][0].data=="EXPRESSION")):
            return 1
        return 0

    def traversing(ast: list):
        for i in range(len(ast)):

            if (start_function(ast[i])):
                f.write("int main(){\n")

            elif (declare_function(ast[i])):
                if (ast[i][1][1][0].data=="NUMBER"):
                    f.write(f"int {ast[i][1][0][1]} = {ast[i][1][1][1]};\n")
                else:
                    f.write(f"string {ast[i][1][0][1]} = {ast[i][1][1][1]};\n")

            elif (print_function(ast[i])):
                f.write(f"cout<<{ast[i][1][1]<<"\n"};\n")

            elif (assign_function(ast[i])):
                # if (ast[i][1][1][0][0].data=="PLUS"):
                f.write(f"{ast[i][1][0][1]} = {ast[i][1][1][1][0][1]} {ast[i][1][1][0][1]} {ast[i][1][1][1][1][1]};\n")

            elif (ifelse_function(ast[i])):
                f.write("if", ast[i][1][0][1], "{ \n")
                traversing (ast[i][2])
                f.write("} \n")
                if (len(ast)==4):
                    f.write("else { \n")
                    traversing(ast[i][3])
                    f.write("} \n")
                    