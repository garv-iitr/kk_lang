from lex import Token

def appendInASTatIndex(indexStorage: list, ast, commands):
    list1 = [ast, 0]
    if (indexStorage == [0]):
        ast.append(commands)
    else:
        for i in indexStorage:
            ast = ast[i]
            list1[1] = ast
        list1[1].append(commands)
        ast = list1[0]



def printTokenCommandCheck(p: list[tuple[Token]], index: int):
    if ((p[index][0].data=="PRINT") and (p[index+1][0].data == "EXPRESSION")):
        return 1
    return 0

def varDeclUninitTokenCommandCheck(p: list[tuple[Token]], index: int):
    if ((p[index][0].data=="VAR_DECL") and (p[index+1][0].data == "ID")):
        if (index+2 < len(p) and p[index+2][0].data != "ASSIGN"):
             return 1
        if (index+2 >= len(p)):
             return 1
    return 0

def varDeclTokenCommandCheck(p: list[tuple[Token]], index: int):
    if ((p[index][0].data=="VAR_DECL") and (p[index+1][0].data == "ID") and (p[index+2][0].data == "ASSIGN") and (p[index+4][0].data=="SEMICOLON")):
        if ((p[index+3][0].data=="NUMBER") or (p[index+3][0].data=="STRING")):
            return 1
    return 0


    return 0

def varInitExprTokenCommandCheck(p: list[tuple[Token]], index: int):
    if ((p[index][0].data=="VAR_DECL") and (p[index+1][0].data == "ID") and (p[index+2][0].data == "ASSIGN")):
         try:
            if ((p[index+4][0].data in ["PLUS", "MINUS", "MULT", "DIV", "MOD", "EE", "GE", "LE", "GT", "LT", "NE"])):
                if ((p[index+3][0].data in["NUMBER","ID","STRING"]) and (p[index+5][0].data in["NUMBER","ID","STRING"])):
                    return 1
         except IndexError:
            return 0
    return 0

def assignTokenCommandCheck(p: list[tuple[Token]], index: int):
    if ((p[index][0].data=="ID") and (p[index+1][0].data == "ASSIGN")):
        if ((p[index+3][0].data in ["PLUS", "MINUS", "MULT", "DIV", "MOD", "EE", "GE", "LE", "GT", "LT", "NE"])):
            if ((p[index+2][0].data in["NUMBER","ID"])and(p[index+4][0].data in["NUMBER","ID"])) or \
            ((p[index+2][0].data)=="STRING"and(p[index+4][0].data=="STRING")):
                return 1
    return 0


def ifelseTokenCommandCheck(p: list[tuple[Token]], index: int):
    if ((p[index][0].data=="IF") and (p[index+1][0].data=="EXPRESSION") and (p[index+2][0].data=="CURLYL")):
        return 1
    return 0
    
def whileTokenCommandCheck(p: list[tuple[Token]], index: int):
    if ((p[index][0].data=="WHILE") and (p[index+1][0].data=="EXPRESSION") and (p[index+2][0].data=="CURLYL")):
        return 1
    return 0

    

    

astg = [(Token("START"), 'khel_shuru')]


def parser(p: list[Token]):
    ast = []
    # print(p)
    if (p[0][0].data == "START"):
        ast = astg
    indexStorage = [[0]]
    TraversalIndexes = [[0]]
    i = 0
    while (i < len(p)):
        if (printTokenCommandCheck(p, i)):
            appendInASTatIndex(indexStorage[-1], ast, [p[i], p[i+1]])
            i += 2
           

        elif (varDeclUninitTokenCommandCheck(p, i)):
            appendInASTatIndex(indexStorage[-1], ast, [p[i], [p[i+1], None]])
            i += 2 
            if i < len(p) and p[i][0].data == "SEMICOLON":
                i += 1
        
        elif (varDeclTokenCommandCheck(p, i)):
            appendInASTatIndex(indexStorage[-1], ast, [p[i], [p[i+1], p[i+3]]])
            i += 4
        

        elif (varInitExprTokenCommandCheck(p, i)):
            appendInASTatIndex(indexStorage[-1], ast, [p[i], [p[i+1], [p[i+4], [p[i+3], p[i+5]]]]])
            i += 6 
            if i < len(p) and p[i][0].data == "SEMICOLON":
                i += 1

        elif (assignTokenCommandCheck(p, i)):
            appendInASTatIndex(indexStorage[-1], ast, [p[i+1], [p[i], [p[i+3], [p[i+2], p[i+4]]]]])
            i += 4

        elif (ifelseTokenCommandCheck(p, i)):
            list1 = []
            j = i+3 
            count_l=1
            
            while (count_l!=0):
                if (p[j][0].data=="CURLYL"):
                    count_l+=1
                elif (p[j][0].data=="CURLYR"):
                    count_l-=1
                list1.append(p[j])
                j += 1
                print(i, j)
            j-=1

            try:
                if (j+1 < len(p) and p[j+1][0].data == "ELSE"):
                    list2 = []
                    j += 2
                    while (p[j][0].data!="CURLYR"):
                        list2.append(p[j])
                        j += 1
                    
                    parsed_list1 = parser(list1)
                    parsed_list2 = parser(list2)
                    parsed_list1.insert(0, (Token("TRUE"), 'true'))
                    parsed_list2.insert(0, (Token("FALSE"), 'false'))
                    command = [p[i], p[i+1], parsed_list1, parsed_list2]
                else:
                    parsed_list1 = parser(list1)
                    parsed_list1.insert(0, (Token("TRUE"), 'true'))
                    command = [p[i], p[i+1], parsed_list1]
                
            except:
                parsed_list1 = parser(list1)
                parsed_list1.insert(0, (Token("TRUE"), 'true'))
                command = [p[i], p[i+1], parsed_list1]

            appendInASTatIndex(indexStorage[-1], ast, command)
            i = j 
        
        elif (whileTokenCommandCheck(p, i)):
            list1 = []
            j = i+3 
            count_l=1
            
            while (count_l!=0):
                if (p[j][0].data=="CURLYL"):
                    count_l+=1
                elif (p[j][0].data=="CURLYR"):
                    count_l-=1
                list1.append(p[j])
                j += 1
            j-=1

            parsed_list1 = parser(list1)
            parsed_list1.insert(0, (Token("TRUE"), 'true'))
            command = [p[i], p[i+1], parsed_list1]
            appendInASTatIndex(indexStorage[-1], ast, command)
            i = j 
            # if (p[j+1][0].data == "ELSE"):
            #     list2 = []
            #     j += 2
            #     while (p[j][0].data!="CURLYR"):
            #         list2.append(p[j])
            #         j += 1
                
            #     parsed_list1 = parser(list1)
            #     print(f"parsed list1 : {parsed_list1}")
            #     parsed_list2 = parser(list2)
            #     print(f"parsed list2 : {parsed_list2}")
            #     parsed_list1.insert(0, (Token("TRUE"), 'true'))
            #     parsed_list2.insert(0, (Token("FALSE"), 'false'))
            #     command = [p[i], p[i+1], parsed_list1, parsed_list2]
            # else:
            #     parsed_list1 = parser(list1)
            #     parsed_list1.insert(0, (Token("TRUE"), 'true'))
            #     command = [p[i], p[i+1], parsed_list1]

            # print("COMMAND:",command)
        elif (p[i][0].data == "SEMICOLON"):
            i+=1
            continue

        elif (p[i][0].data == "CURLYR"):
            i+=1
            continue

        elif (p[i][0].data == "END"):
            return ast
        
        elif (p[i][0].data == "START"):
            i += 1
            continue


        i += 1
        # print(i)
        # print(p[i][1])

    return ast
    

        
            
                
            

    # elif (p[0].data == "START"):
    #     print("Khel toh shuru karo")
    # else:
    #     print("Khel toh khatam karo")

    





if (__name__ == "__main__"):
    from lex import lex
    f = open("input.txt", "r")
    p = lex(f)
    print("p : [", end="")
    for i in range(len(p)):
            if (i == len(p)-1):
                print(p[i][0].data, ":", p[i][1], end="") 
            else:
                print(p[i][0].data, ":", p[i][1], end=", ")
    print("]")
    ast_ = parser(p)
    print("AST: ")
    print(ast_)



# [START : khel_shuru, PRINT : elaan_karo, EXPRESSION : (x), SEMICOLON : ;, VAR_DECL : khiladi, ID : x, ASSIGN : =, NUMBER : 10, SEMICOLON : ;, ID : x, ASSIGN : =, ID : x, PLUS : +, NUMBER : 10, SEMICOLON : ;, PRINT : elaan_karo, EXPRESSION : (x), SEMICOLON : ;, END : khel_khatam]