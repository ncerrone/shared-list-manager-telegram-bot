import logging
import requests
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import os
import sqlite3

# Set up basic logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "TOKEN"
DB_NAME = "bot_data.db"

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def init_db():
    """DB init (SQLite database)"""
    try:
        conn =  sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS films (
                id INTEGER PRIMARY KEY,
                filmName TEXT
                )"""
        )
        conn.commit()
        conn.close()
    except Exception as e :
        print(f"Errore connessione DB... {e}")
        
        
init_db()


def send_message(chat_id, text):
    response = requests.post(
        f"{BASE_URL}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
        },
        timeout=30,
    )
    response.raise_for_status()
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    user = update.effective_user
    await update.message.reply_html(
        f"Ciao {user.mention_html()}! Benvenuto in un comodo strumento di gestione di liste condivise per coppie," \
                 " amici e gruppi più o meno grandi di persone. Enjoy!"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles all non-command text messages."""
    await update.message.reply_text(f"Hai scritto: {update.message.text}")
    

async def add_film(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets a user preference with validation and database persistence."""
    await update.message.reply_text(f"Non ancora implementato...")
    # user_id = update.effective_user.id
    
    # if not context.args:
    #     # Validation
    #     await update.message.reply_text("Must provide a preference. Usage: /set_pref <value>")
    #     return
        
    # preference = " ".join(context.args).strip()
    
    # try:
    #     conn = sqlite3.connect(DATABASE_NAME)
    #     cursor = conn.cursor()
        
    #     # SQL INSERT OR REPLACE statement for persistence
    #     cursor.execute(
    #         "INSERT OR REPLACE INTO users (id, preference) VALUES (?, ?)", 
    #         (user_id, preference)
    #     )
    #     conn.commit()
    #     conn.close()
        
    #     # Basic State Management
    #     context.user_data['preference'] = preference
        
    #     await update.message.reply_text(f"Preference saved: {preference}")
        
    # except Exception as e:
    #     logger.error(f"Database error: {e}")
    #     await update.message.reply_text("Sorry, ran into a database error while saving.")

async def get_film_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Retrieves and displays the userʼs saved film list."""
    user_id = update.effective_user.id
        
    # Check the persistent database
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT filmName FROM films")
        result = cursor.fetchall()
        conn.close()
        
        if result:
            await update.message.reply_text(f"From the DB: I film salvati sono: {result}")
        else:
            await update.message.reply_text("Non hai ancora inserito nessun film alla lista. Use /set_pref!")
            
    except Exception as e:
        logger.error(f"Database error: {e}")
        await update.message.reply_text("Sorry, ran into a database error while retrieving.")


# offset = None -- used in the original boilerplate used at the end of this file --> to be removed

app = Application.builder().token(TOKEN).build()
# Run the bot
logger.info("Bot starting...")

def main() -> None:
    """Starts the bot application."""
    app = Application.builder().token(TOKEN).build()
    # Run the bot
    logger.info("Bot starting...")

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_film", add_film))
    app.add_handler(CommandHandler("get_film_list", get_film_list)) 
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

# while True:
#     try:
#         params = {
#             "timeout": 30,
#         }

#         if offset is not None:
#             params["offset"] = offset

#         response = requests.get(
#             f"{BASE_URL}/getUpdates",
#             params=params,
#             timeout=35,
#         )
#         response.raise_for_status()

#         data = response.json()

#         for update in data.get("result", []):
#             offset = update["update_id"] + 1

#             message = update.get("message")

#             if not message:
#                 continue

#             chat_id = message["chat"]["id"]
#             text = message.get("text", "")

#             if text == "/start":
#                 reply = (
#                     "Benvenuto in un comodo strumento di gestione di liste condivise per coppie," \
#                     " amici e gruppi più o meno grandi di persone. Enjoy!"
#                 )

#             elif text == "/help":
#                 reply = (
#                     "Comandi disponibili:\n"
#                     "/start - Avvia il bot\n"
#                     "/help - Mostra i comandi\n"
#                     "/next - Nuove funzionalità previste\n"
#                     "/requests - Aggiungi suggerimenti per nuove funzionalità\n"
#                     "/info - Mostra le informazioni del bot\n"
#                     "/contatti - Mostra le informazioni di contatto e supporto\n"
#                     "/film - Gestione della funzionalità di lista film"
#                 )

#             elif text == "/next":
#                 reply = "Per il momento i prossimi rilasci sono in standby, attendere."

#             elif text == "/film":
#                 reply = "Non ancora implementato, attendere..."
                
#                 conn =  sqlite3.connect(DB_NAME)
                
#                 cursor = conn.cursor()
#                 cursor.execute(
#             "INSERT OR REPLACE INTO films (id, filmName) VALUES (?, ?)"
#                 ), (1, 'aa')
#                 conn.commit()
#                 conn.close()
                
#                 reply = "Salvato"
                
                
#             elif text == "/requests":
#                 reply = "Non ancora implementato, attendere..."

#             elif text:
#                 reply = f"Hai scritto: {text}"

#             else:
#                 reply = "Per il momento posso leggere solo messaggi di testo."

#             send_message(chat_id, reply)

#     except requests.RequestException as error:
#         print(f"Errore di rete: {error}")
#         time.sleep(5)