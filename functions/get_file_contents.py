import os
from config import MAX_CHARS


def get_file_contents(working_directory, file_path=None):
    abs_path = os.path.abspath(working_directory)
    target_file = abs_path
    if file_path:
        target_file = os.path.abspath(os.path.join(abs_path, file_path))
    if not target_file.startswith(abs_path):
        return f'Error: Cannot read {file_path} as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        print(target_file)
        return f'Error: File not found or is not a regular file'

    try:
        with open(target_file, 'r') as f:
            file_content = f.read(MAX_CHARS)
            return file_content
    except Exception as e:
        return f'Error reading file: {e}'
