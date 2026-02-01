from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sys
import subprocess
import os
import tempfile
import shutil

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 256 * 1024 * 1024 

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["1000 per day", "100 per hour"],
    storage_uri="memory://"
)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large (Max 1MB)'}), 413

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': f"Rate limit exceeded: {e.description}"}), 429

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/compile', methods=['POST', 'OPTIONS'])
@limiter.limit("50 per minute")
def compile_code():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({'error': 'No code provided'}), 400

    code = data['code']
    output_cpp = ""
    output_txt = ""

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            shutil.copy('main.py', os.path.join(temp_dir, 'main.py'))
            shutil.copy('lex.py', os.path.join(temp_dir, 'lex.py'))
            shutil.copy('kk_parser.py', os.path.join(temp_dir, 'kk_parser.py'))
            shutil.copy('transpiler.py', os.path.join(temp_dir, 'transpiler.py'))
            
            with open(os.path.join(temp_dir, 'input.txt'), 'w') as f:
                f.write(code)

            docker_cmd = [
                'docker', 'run', '--rm',              
                '--network', 'none',                  
                '--memory', '256m',                   
                '--cpus', '0.5',                      
                '-v', f'{temp_dir}:/app',             
                'khelkhatam-runner',                  
                'python3', 'main.py'                  
            ]

            result = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=10) # 10s timeout
            
            if result.returncode != 0:
                error_log = f"Execution Error:\n{result.stderr}\n{result.stdout}"
                out_txt_path = os.path.join(temp_dir, 'output.txt')
                if os.path.exists(out_txt_path):
                     with open(out_txt_path, 'r') as f:
                        error_log += "\n\n" + f.read()
                
                return _corsify_actual_response(jsonify({'error': 'Sandbox Execution Failed', 'details': error_log})), 500

            out_cpp_path = os.path.join(temp_dir, 'output.cpp')
            out_txt_path = os.path.join(temp_dir, 'output.txt')

            if os.path.exists(out_cpp_path):
                with open(out_cpp_path, 'r') as f:
                    output_cpp = f.read()
            
            if os.path.exists(out_txt_path):
                with open(out_txt_path, 'r') as f:
                    output_txt = f.read()
            else:
                output_txt = result.stdout or "No output generated."

        except subprocess.TimeoutExpired:
            return _corsify_actual_response(jsonify({'error': 'Execution Timed Out (Max 10s)'})), 500
        except Exception as e:
            return _corsify_actual_response(jsonify({'error': f'Server Internal Error: {str(e)}'})), 500

    return _corsify_actual_response(jsonify({
        'cpp': output_cpp,
        'output': output_txt
    }))

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
