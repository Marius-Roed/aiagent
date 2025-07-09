import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_info import get_files_info


def main():
    if len(sys.argv) < 2:
        print('Usage: uv run main.py <prompt>')
        sys.exit(1)

    user_prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')

    client = genai.Client(api_key=api_key)

    resp = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages
    )

    print(resp.text)

    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {resp.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
