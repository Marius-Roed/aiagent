import os


def write_file(working_directory, file_path, content):
    abs_path = os.path.abspath(working_directory)
    target_file = abs_path
    if file_path:
        target_file = os.path.abspath(os.path.join(abs_path, file_path))
    if not target_file.startswith(abs_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        base_dir = os.path.dirname(target_file)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        with open(target_file, 'w') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error writing to file: {e}"
