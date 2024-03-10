import openai
from dotenv import load_dotenv
import os
import pyttsx3
import speech_recognition as sr

# isso aq é pra carregar sua KEY q ta no .env
load_dotenv()
openai.api_key = os.getenv("OPEN_AI_KEY")

# função para capturar sua voz do microfone
def ouvir_microfone():
    microfone = sr.Recognizer()

    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source)

        print("Estou ouvindo: ")

        audio = microfone.listen(source)

    try:
        frase = microfone.recognize_google(audio, language='pt-BR')
        print("Você disse: " + frase)
        return frase
    except sr.UnknownValueError:
        print("Não entendi")
        return None

# função para usar a IA com a API OpenAI
def ask_gpt(mensagens, frase):
    mensagens = [mensagens[0]] + mensagens[-10:] + [{"role": "user", "content": frase}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=mensagens,
        max_tokens=500,
        temperature=1
    )
    return response['choices'][0]['message']['content']

# função principal
def main():
    # define as variáveis
    nome = "Unknown"
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) # define a voz desejada *nao q tenha muitas opções né*

    # mensagem inicial, onde o bot assume uma "personalidade"
    mensagens = [{"role": "system", "content": f"Seu nome é {nome} você é uma inteligencia artificial feita para educação de crianças. Por tanto responderá dúvidas e poderá contar histórias."},]

    while True:
        # captura a voz do usuário
        frase = ouvir_microfone()

        # se a frase for válida
        if frase is not None:
            # adiciona a mensagem do usuário na lista
            mensagens.append({"role": "user", "content": frase})

            # envia a frase para a API OpenAI e recebe a resposta
            resposta = ask_gpt(mensagens, frase)

            # adiciona a resposta do sistema à lista
            mensagens.append({"role": "system", "content": resposta})

            # exibe a resposta na tela e reproduz em voz alta
            print(f"{nome}:", resposta)
            engine.say(resposta)
            engine.runAndWait()

# executa a função principal
if __name__ == "__main__":
    main()
