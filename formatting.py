import os

def format():
    base = os.path.dirname(__file__)
    out_path = os.path.join(base, "output.cpp")

    with open(out_path, 'r') as f:
        all_lines = f.readlines()

    print("all lines : ",all_lines)
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
    f.seek(0)
    f.writelines(new_lines)
    f.close()