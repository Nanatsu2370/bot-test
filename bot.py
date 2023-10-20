import telebot
from telebot import types
from tqdm import tqdm
import requests

# Configura tu token de acceso al bot
TOKEN = '6525649877:AAF6mqeaMsIglYA1OToV6ZJhXLeo3q-okr0'

# Crea una instancia del bot de Telegram
bot = telebot.TeleBot(TOKEN)

# Función para manejar el comando /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, '¡Hola! Envíame el enlace del archivo que deseas descargar.')

# Función para manejar el enlace del archivo
@bot.message_handler(func=lambda message: True)
def download_file(message):
    # Verifica si el mensaje contiene un enlace válido
    if message.text.startswith('http'):
        file_url = message.text

        # Descarga el archivo y muestra el progreso utilizando tqdm
        response = requests.get(file_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open('archivo_descargado', 'wb') as file:
            # Muestra el progreso utilizando tqdm
            with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
                for chunk in response.iter_content(32 * 1024):
                    if chunk:
                        file.write(chunk)
                        pbar.update(len(chunk))

        # Envía el archivo descargado
        with open('archivo_descargado', 'rb') as file:
            bot.send_document(message.chat.id, file)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    # Descargar documento y mostrar su progreso
    file_info = bot.get_file(message.document.file_id)
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

    response = requests.get(file_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open('archivo_descargado', 'wb') as file:
        with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
            for chunk in response.iter_content(32 * 1024):
                if chunk:
                    file.write(chunk)
                    pbar.update(len(chunk))

    # Envía el archivo descargado
    with open('archivo_descargado', 'rb') as file:
        bot.send_document(message.chat.id, file)


# Inicia el bot
bot.polling()
