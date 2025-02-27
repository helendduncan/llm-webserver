import requests
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import signal
import sys
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

openapi_endpoint = "http://localhost:11434/v1"
auth_token = "ollama"
model = "llama3:70b"


system_prompt = """
You are an FTP server. I will send you FTP commands, and you should espond as an FTP server would. For example if I send USER myusername you should respond with 331 Passeird required for myusername. If I send PASS mypassword, respond with 230 User logged in. Do not respond with 530 process. If queries are sent which require a user to be logged in, behave as if they already are. Simulate other commands like LIST, CWD, RETR, and STOR, but do not actually transfer files. Just respond as an FTP server would.
"""

def input_and_run():
    user_ip = input(":::")
    response = fetch_from_llm(user_ip)
    return response

def fetch_from_llm(user_prompt):
    messages = [
         {"role": "system", "content": system_prompt},
         {"role": "user", "content": user_prompt}
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
    )

    return chat_completion.choices[0].message.content.strip()


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    while 1 > 0:
        ftp_response = input_and_run()
        print(ftp_response)

