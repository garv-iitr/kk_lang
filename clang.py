import subprocess
import os

def run_clang_pipeline(source_file):

    output_bin = "compiled_output"
    if (os.name!="nt"):
        compile_cmd = ["clang++", source_file, "-o", output_bin]
    else:
        compile_cmd = ["g++", source_file, "-o", output_bin]
        
    compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True)
    
    if compile_proc.returncode != 0:
        print("Compilation Failed!")
        print(compile_proc.stderr)
        return

    try:
        exec_path = f"./{output_bin}" if os.name != "nt" else output_bin
        run_proc = subprocess.run([exec_path], capture_output=True, text=True)
        print("Execution Output:")
        print(run_proc.stdout)
        
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        if os.path.exists(output_bin):
            os.remove(output_bin)

if __name__ == "__main__":
    if os.path.exists("input.cpp"):
        run_clang_pipeline("input.cpp")
    else:
        print("Error: 'input.cpp' not found in the current directory.")