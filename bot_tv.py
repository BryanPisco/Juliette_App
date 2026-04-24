import telebot
import subprocess
import re
import os

# === CONFIGURACIÓN ===
TOKEN = '8631518314:AAFG6jhIbwHt_3XeU_wh8Wv0ry8m0TzNtP8'
MI_CHAT_ID = 7124486834
# Nombres exactos obtenidos de tu xinput list
DISPOSITIVOS_OBJETIVO = [
    "AT Translated Set 2 keyboard",
    "DELL0978:00 04F3:30C3 Touchpad"
]

bot = telebot.TeleBot(TOKEN)

def gestionar_perifericos(accion):
    """
    Busca los IDs de los dispositivos específicos y aplica 'enable' o 'disable'.
    Retorna la cantidad de dispositivos procesados con éxito.
    """
    procesados = 0
    try:
        # Obtenemos la lista de xinput
        salida = subprocess.check_output(['xinput', 'list'], env={'DISPLAY': ':0'}, text=True)
        
        for nombre in DISPOSITIVOS_OBJETIVO:
            for linea in salida.split('\n'):
                # Buscamos la coincidencia exacta del nombre en la línea
                if nombre in linea:
                    match = re.search(r'id=(\d+)', linea)
                    if match:
                        id_dev = match.group(1)
                        # Ejecutamos la acción (disable/enable)
                        subprocess.run(['xinput', accion, id_dev], env={'DISPLAY': ':0'})
                        procesados += 1
                        break # Pasamos al siguiente dispositivo de nuestra lista
        return procesados
    except Exception as e:
        print(f"Error en gestionar_perifericos: {e}")
        return 0

@bot.message_handler(commands=['start'])
def enviar_bienvenida(message):
    if message.chat.id == MI_CHAT_ID:
        bot.reply_to(message, "¡TV Control Brave Activo! 📺\n\n/play [url] - Abrir video\n/stop - Cerrar Brave\n/bloquear - Off Teclado\n/desbloquear - On Teclado")

@bot.message_handler(commands=['play'])
def play_video(message):
    if message.chat.id != MI_CHAT_ID: return
    
    partes = message.text.split(' ')
    if len(partes) > 1:
        url = partes[1].strip()
        bot.reply_to(message, "Cambiando video... 📺")
        
        # 1. Matamos cualquier instancia previa de Brave para limpiar la pantalla
        # Esto evita que se acumulen ventanas y sonidos.
        subprocess.run(["pkill", "brave"])
        
        # 2. Comando Modo App:
        # --app: Abre la URL en una ventana limpia sin interfaz de navegador.
        # --start-fullscreen: Fuerza que esa ventana ocupe toda la pantalla.
        # --autoplay-policy=no-user-gesture-required: Intenta forzar el inicio automático.
        comando = [
            "brave-browser", 
            f"--app={url}", 
            "--start-fullscreen", 
            "--autoplay-policy=no-user-gesture-required"
        ]
        
        try:
            subprocess.Popen(comando, env={**os.environ, "DISPLAY": ":0"})
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")
    else:
        bot.reply_to(message, "Uso: /play [link]")
@bot.message_handler(commands=['stop'])
def stop_video(message):
    if message.chat.id == MI_CHAT_ID:
        # Cerramos todas las instancias de Brave
        subprocess.run(["pkill", "brave"])
        bot.reply_to(message, "Brave cerrado. ⏹️")

@bot.message_handler(commands=['bloquear'])
def bloquear(message):
    if message.chat.id == MI_CHAT_ID:
        exitos = gestionar_perifericos('disable')
        if exitos > 0:
            bot.reply_to(message, f"🔒 Bloqueo activo ({exitos}/{len(DISPOSITIVOS_OBJETIVO)} disp.)\nTeclado y Touchpad desactivados.")
        else:
            bot.reply_to(message, "⚠️ No se pudo bloquear ningún dispositivo. Revisa la terminal de la laptop.")

@bot.message_handler(commands=['desbloquear'])
def desbloquear(message):
    if message.chat.id == MI_CHAT_ID:
        exitos = gestionar_perifericos('enable')
        if exitos > 0:
            bot.reply_to(message, "🔓 Teclado y Touchpad reactivados.")
        else:
            bot.reply_to(message, "⚠️ No se pudo reactivar los dispositivos.")

print("Bot iniciado y esperando órdenes...")
bot.infinity_polling(timeout=10, long_polling_timeout=5)