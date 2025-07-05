import os
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')

    client = genai.Client(api_key=api_key)

    resp = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents="Why is Boot.dev such a great place to learn backend developement. Use one paragraph maximum"
    )

    print(resp.text)

    print("Proompt tokens: " + resp.usage_metadata.prompt_token_count)
    print("Resp tokens: " + resp.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
