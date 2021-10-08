from flask import Flask
from threading import Thread
import discord

app = Flask('')

@app.route('/')
def home():
    msg = f"Bot is Active... discord.py Version: v{discord.__version__}"
    return msg

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()