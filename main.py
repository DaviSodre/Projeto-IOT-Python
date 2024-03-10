import openai
from dotenv import load_dotenv
import os

load_dotenv()


openai.api_key = os.getenv("OPEN_AI_KEY")

nome = "Unknown"

mensagens = [{"role": "system", "content": f"Seu nome é {nome} você é uma inteligencia artificial feita para educação de crianças. Por tanto responderá dúvidas e poderá contar histórias."},]

def ask_gpt(mensagens, user_input):
    mensagens = mensagens + [{"role": "user", "content": user_input}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=mensagens,
        max_tokens=250,
        temperature=1
    )
    return response['choices'][0]['message']['content']

def main():
    while True:
        user_input = input("Você: ")
        resposta = ask_gpt(mensagens, user_input)
        print(f"{nome}:", resposta)

if __name__ == "__main__":
    main()
