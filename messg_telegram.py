import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from escaner_red import Scanner
from basedatos import database

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN_TELEGRAM")
ADMIN = os.getenv("ADMIN_ID")
logging.basicConfig(level=logging.INFO)


teclado = [["/ayuda"],["/scann"],["/dbhosts"]]
reply_markup = ReplyKeyboardMarkup(teclado,resize_keyboard=True)

def es_admin(update: Update) -> bool:
    return update.effective_user.id == int(ADMIN)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if not es_admin(update):
        await update.message.reply_text(f"Lo siento esto es un bot personal.")
        return
        
    await update.message.reply_text(f"Hola bienvenido a {update.effective_user.first_name}, soy tu bot. Prueba /ayuda.")
    await update.message.reply_text(f" Menu:",reply_markup=reply_markup)

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if not es_admin(update):
        await update.message.reply_text(f"Lo siento esto es un bot personal.")
        return
    await update.message.reply_text("Comandos disponibles\n" "/ayuda - Muestra esta ayuda\n" "/scann - Hace un escaneo para ver la red de casa\n" "/dbhosts - Ver la base de datos de equipos")

async def scann(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    if not es_admin(update):
        await update.message.reply_text(f"Lo siento esto es un bot personal.")
        return
    
    escaner = Scanner("192.168.1.0/24")
    equipos = escaner.texto_lista_equipos_vivos()
    await update.message.reply_text(equipos)

async def dbhosts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not es_admin(update):
        await update.message.reply_text(f"Lo siento esto es un bot personal.")
        return
    conexion = database("database.db")
    datos = conexion.select("*","")
    texto = "Indice | MAC | IP | Hostname | Fabricante | 1º con | ult con\n"
    texto += "-------------------------------------------------------------------------------------------\n"
    for i,filas in enumerate(datos):
        texto += f"{i+1}. {filas[2]} | {filas[1]} | {filas[3]} | {filas[4]} | {filas[5]} | {filas[6]} \n\n"
    await update.message.reply_text(str(texto))


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("scann", scann))
    app.add_handler(CommandHandler("dbhosts",dbhosts))


    app.run_polling()


if __name__ == '__main__':
    main()