import os
import asyncio
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WHALE_WALLET = "0xYOUR_WALLET_ADDRESS_HERE" # <-- CHANGE THIS

RPC_LIST = ["https://bsc-dataseed.binance.org/", "https://rpc.ankr.com/bsc"]
BSC_RPC = None
last_block = 0

for rpc in RPC_LIST:
    try:
        r = requests.post(rpc, json={"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}, timeout=5)
        last_block = int(r.json()['result'], 16)
        BSC_RPC = rpc
        print(f"Connected to BSC! Block: {last_block} via {rpc}")
        break
    except: continue

def get_buttons():
    keyboard = [[InlineKeyboardButton("📊 Chart", url="https://poocoin.app")]]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🚀 Bot LIVE! Watching: {WHALE_WALLET[:10]}...", reply_markup=get_buttons())

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    await app.run_polling()

asyncio.run(main())
