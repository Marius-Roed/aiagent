import os
import subprocess


def run_python_file(working_directory, file_path, timeout=30):
    abs_path = os.path.abspath(working_directory)
    target_file = abs_path
    if file_path:
        target_file = os.path.abspath(os.path.join(abs_path, file_path))
    if not target_file.startswith(abs_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'
    if not target_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        p = subprocess.run(["uv", "run", target_file],
                           timeout=timeout, capture_output=True)
        output = []
        if len(p.stdout) > 0:
            output.append(f"STDOUT: {p.stdout}")
        else:
            output.append("STDOUT: No output produced")
        output.append(f"STDERR: {p.stderr}")
        if p.returncode:
            output.append(f"Process exited with code {p.returncode}")
        return "\n".join(output)
    except Exception as e:
        return f'Error runing pyton file "{file_path}": {e}'
