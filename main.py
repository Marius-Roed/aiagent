import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_info import get_files_info
from functions.get_file_contents import get_file_contents
from functions.write_file import write_file
from functions.run_python import run_python_file
from config import MAX_CHARS


def call_function(function_call_part, verbose="false"):
    if verbose:
        print(f"Calling function: {
              function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    output = ""

    try:
        match function_call_part.name:
            case "get_files_info":
                output = get_files_info(
                    "calculator", **function_call_part.args)
            case "get_file_contents":
                output = get_file_contents(
                    "calculator", **function_call_part.args)
            case "write_file":
                output = write_file("calculator", **function_call_part.args)
            case "run_python_file":
                output = run_python_file(
                    "calculator", **function_call_part.args)
            case _:
                ValueError("Function unknown")

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": output},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {
                        function_call_part.name}"},
                )
            ],
        )


def main():
    verbose = False
    if len(sys.argv) < 2:
        print('Usage: uv run main.py <prompt>')
        sys.exit(1)

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    user_prompt = sys.argv[1]

    schema_get_file_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_get_file_contents = types.FunctionDeclaration(
        name="get_file_contents",
        description=f"Lists the file contents of the specified path, relative to the working directory. File contents {
            MAX_CHARS} characters above will be truncated.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file, which contents should be listed, relative to the working directory",
                ),
            },
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes to a file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file path": types.Schema(
                    type=types.Type.STRING,
                    description="The path of the file which should be written to.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The contents which should be written to the file. If the file doesn't already exist, it will be created.",
                ),
            },
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a python file with optional arguments, and lists the output, plus its exit code.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The relative file path from the working directory which should be executed by the python interpretter",
                ),
            },
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_file_info,
            schema_get_file_contents,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')

    client = genai.Client(api_key=api_key)

    resp = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    if "--verbose" in sys.argv:
        verbose = True

    if resp.function_calls and len(resp.function_calls) > 0:
        for function_call_part in resp.function_calls:
            function_result = call_function(function_call_part, verbose)
            print(f"-> {function_result.parts[0].function_response.response}")
    if (resp.text):
        print(resp.text)

    if verbose:
        print("")
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {resp.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
