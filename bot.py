import os
import asyncio
import requests
from web3 import Web3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ====== LOAD SECRETS FROM RAILWAY VARIABLES ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BSC_RPC = os.getenv("BSC_RPC")

# ====== CONFIG ======
WHALE_WALLET = "0x822c562a19317e9c61269C0Fdab90E48AA43Fc6F"  # <-- CHANGE THIS TO YOUR WALLET
KOMA_CONTRACT = "0x55d398326f99059fF775485246999027B3197955"  # USDT for testing

print("Connecting to BSC...")
w3 = Web3(Web3.HTTPProvider(BSC_RPC))

if not w3.is_connected():
    print("ERROR: Could not connect to BSC RPC")
    exit()

print("Connected to BSC!")
last_block = w3.eth.block_number

# ====== BUTTONS ======
def get_buttons():
    keyboard = [
        [InlineKeyboardButton("📊 Chart", url=f"https://poocoin.app/tokens/{KOMA_CONTRACT}")],
        [InlineKeyboardButton("💎 Buy", url=f"https://pancakeswap.finance/swap?outputCurrency={KOMA_CONTRACT}")],
        [InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== COMMANDS ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🚀 *KOMA Whale Bot is LIVE* 🚀\n\nWatching: `{WHALE_WALLET[:10]}...`",
        reply_markup=get_buttons(),
        parse_mode="Markdown"
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "refresh":
        await query.edit_message_text("🔄 Refreshed!", reply_markup=get_buttons())

# ====== WHALE TRACKER ======
async def check_whale():
    global last_block
    while True:
        try:
            current_block = w3.eth.block_number
            if current_block > last_block:
                print(f"New block: {current_block}")
                last_block = current_block
            await asyncio.sleep(10)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(20)

# ====== RUN BOT ======
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    asyncio.create_task(check_whale())
    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
