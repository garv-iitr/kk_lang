
import sys
import os
import subprocess
from kk_parser import parser
from lex import lex
from transpiler import traversing
import transpiler

def main():
    try:
        f = open("input.txt", "r")
    except FileNotFoundError:
        print("Error: input.txt not found")
        sys.exit(1)

    try:
        p = lex(f)
        ast = parser(p)
        traversing(ast) 
        transpiler.f.close()
        f.close()

        f_cpp = open("output.cpp","r")
        all_lines = f_cpp.readlines()
        f_cpp.close()

        new_lines = []
        c = 0
        curlyopen = 0
        curlyclose = 0

        for line in all_lines:
            line = line.strip()

            curlyopen = 0
            curlyclose = 0
            
            for char in line:
                if (char == "{"):
                    c += 1
                    curlyopen = 1
                elif (char == "}"):
                    c -= 1
                    curlyclose = 1
            
            indent = ""
            if (curlyclose == 1):
                indent = c * "\t"
            elif (curlyopen == 1):
                indent = (c - 1) * "\t"
            else:
                indent = c * "\t"
            
            new_lines.append(indent + line + "\n")
        
        f_cpp = open("output.cpp","w")
        f_cpp.writelines(new_lines)
        f_cpp.close()

    except Exception as e:
        with open("output.txt", "w") as err_f:
            err_f.write(f"Transpilation Error:\n{str(e)}")
        sys.exit(1)

    compile_cmd = ["g++", "output.cpp", "-o", "prog"]
    
    try:
        subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        with open("output.txt", "w") as f:
            f.write(f"Compilation Error:\n{e.stderr}")
        return

    run_cmd = ["./prog"]
    if os.name == 'nt':
        run_cmd = ["prog.exe"]

    try:
        result = subprocess.run(run_cmd, capture_output=True, text=True)
        with open("output.txt", "w") as f:
            f.write(result.stdout)
            if result.stderr:
                f.write("\nRuntime Errors:\n" + result.stderr)
                
    except Exception as e:
        with open("output.txt", "a") as f:
            f.write(f"Execution failed: {str(e)}")

if __name__ == "__main__":
    main()
