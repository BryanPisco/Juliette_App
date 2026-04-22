import telebot
import subprocess
import re
import os

# === CONFIGURACIÓN ===
TOKEN = '8631518314:AAFG6jhIbwHt_3XeU_wh8Wv0ry8m0TzNtP8'
MI_CHAT_ID = 7124486834
NOMBRE_TECLADO = "AT Translated Set 2 keyboard"

bot = telebot.TeleBot(TOKEN)

def ejecutar_comando_xinput(accion):
    """Accion puede ser 'enable' o 'disable'"""
    try:
        # Buscamos el ID dinámicamente cada vez por si cambia
        salida = subprocess.check_output(['xinput', 'list'], env={'DISPLAY': ':0'}, text=True)
        for linea in salida.split('\n'):
            if NOMBRE_TECLADO in linea:
                match = re.search(r'id=(\d+)', linea)
                if match:
                    id_dispositivo = match.group(1)
                    subprocess.run(['xinput', accion, id_dispositivo], env={'DISPLAY': ':0'})
                    return True
        return False
    except Exception as e:
        print(f"Error en xinput: {e}")
        return False

@bot.message_handler(commands=['start'])
def enviar_bienvenida(message):
    if message.chat.id == MI_CHAT_ID:
        bot.reply_to(message, "¡TV de mi hija lista! 📺\nComandos:\n/play [url]\n/stop\n/bloquear\n/desbloquear")

@bot.message_handler(commands=['play'])
def play_video(message):
    if message.chat.id != MI_CHAT_ID: return
    
    # Separamos el comando del link y limpiamos espacios
    partes = message.text.split(' ')
    if len(partes) > 1:
        url = partes[1].strip()
        bot.reply_to(message, "Procesando enlace... 📺")
        
        # Detenemos cualquier video previo
        subprocess.run(["pkill", "mpv"])
        
        # Ruta absoluta al yt-dlp de tu entorno virtual
        ruta_ytdlp = os.path.expanduser("~/control_tv/venv/bin/yt-dlp")
        
        # Comando mejorado:
        # --fs: pantalla completa
        # --force-window: asegura que se abra la ventana aunque tarde en cargar
        # --ytdl-path: le dice exactamente donde está el motor de YouTube
        comando = [
            "mpv", 
            "--fs", 
            "--force-window",
            f"--ytdl-path={ruta_ytdlp}", 
            url
        ]
        
        try:
            # Usamos env={"DISPLAY": ":0"} para que sepa en qué pantalla abrirse
            subprocess.Popen(comando, env={**os.environ, "DISPLAY": ":0"})
        except Exception as e:
            bot.reply_to(message, f"Error al lanzar el reproductor: {e}")
    else:
        bot.reply_to(message, "Uso: /play [link]")

@bot.message_handler(commands=['stop'])
def stop_video(message):
    if message.chat.id == MI_CHAT_ID:
        subprocess.run(["pkill", "mpv"])
        bot.reply_to(message, "Video detenido. ⏹️")

@bot.message_handler(commands=['bloquear'])
def bloquear(message):
    if message.chat.id == MI_CHAT_ID:
        if ejecutar_comando_xinput('disable'):
            bot.reply_to(message, "Teclado BLOQUEADO 🔒")
        else:
            bot.reply_to(message, "No se encontró el teclado.")

@bot.message_handler(commands=['desbloquear'])
def desbloquear(message):
    if message.chat.id == MI_CHAT_ID:
        if ejecutar_comando_xinput('enable'):
            bot.reply_to(message, "Teclado DESBLOQUEADO 🔓")
        else:
            bot.reply_to(message, "No se encontró el teclado.")

print("Bot iniciado y esperando órdenes...")
bot.infinity_polling()