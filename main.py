import openai
from dotenv import load_dotenv
import os
import gtts
from playsound import playsound
import time

load_dotenv()


openai.api_key = os.getenv("OPEN_AI_KEY")

nome = "Unknown"
conversa = []  # lista para guardar a conversa

mensagens = [{"role": "system", "content": f"Seu nome é {nome} você é uma inteligencia artificial feita para educação de crianças. Por tanto responderá dúvidas e poderá contar histórias."},]

def ask_gpt(mensagens, user_input):
    mensagens = [mensagens[0]] + mensagens[-10:] + [{"role": "user", "content": user_input}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=mensagens,
        max_tokens=500,
        temperature=1
    )
    return response['choices'][0]['message']['content']

def main():
    while True:
        user_input = input("Você: ")
        mensagens.append({"role": "user", "content": user_input})  # Adiciona a mensagem do usuário à lista    
        resposta = ask_gpt(mensagens, user_input)
        mensagens.append({"role": "system", "content": resposta})  # Adiciona a resposta do sistema à lista
        print(f"{nome}:", resposta)
        
        falar = gtts.gTTS(resposta, lang='pt-br')
        falar.save('audio.mp3')
        time.sleep(1) # Para tentar resolver o bug de dar erro ao reproduzir o audio
        playsound('audio.mp3')
        os.remove('audio.mp3')
        


if __name__ == "__main__":
    main()


