def format():
    f=open("output.cpp","r")
    all_lines=f.readlines()
    f.close()

    new_lines=[]

    c=0
    curlyopen=0
    curlyclose=0

    for line in all_lines:
        for char in line:
            if (char=="{"):
                c+=1
                curlyopen=1
            elif (char=="}"):
                c-=1
                curlyclose=1
        if (curlyclose==1):
            new_lines.append(c*"\t"+line)
        elif (curlyopen==1):
            new_lines.append((c-1)*"\t"+line)
        else:
            new_lines.append((c)*"\t"+line)
        curlyopen=0
        curlyclose=0
    f=open("output.cpp","w")
    f.writelines(new_lines)
    f.close()