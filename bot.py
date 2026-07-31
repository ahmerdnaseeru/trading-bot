import os
import asyncio
import requests
from web3 import Web3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ====== LOAD SECRETS FROM RENDER ======
BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
BSC_RPC = os.environ.get("BSC_RPC")

# ====== CONFIG ======
KOMA_CONTRACT = "0x822c562a19317e9c61269C0Fdab90E48AA43Fc6F"  # <-- PUT YOUR KOMA TOKEN ADDRESS HERE
WHALE_WALLET = "0x822c562a19317e9c61269C0Fdab90E48AA43Fc6F"    # <-- PUT THE WHALE WALLET HERE

w3 = Web3(Web3.HTTPProvider(BSC_RPC))
last_block = w3.eth.block_number

# ====== BUTTONS ======
def get_buttons():
    keyboard = [
        [InlineKeyboardButton("📊 Chart", url=f"https://poocoin.app/tokens/{KOMA_CONTRACT}")],
        [InlineKeyboardButton("💎 Buy KOMA", url=f"https://pancakeswap.finance/swap?outputCurrency={KOMA_CONTRACT}")],
        [InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== COMMANDS ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 *KOMA Whale Bot is LIVE* 🚀\n\nWatching whale: " + WHALE_WALLET[:10] + "...",
        reply_markup=get_buttons(),
        parse_mode="Markdown"
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "refresh":
        await query.edit_message_text("🔄 Refreshed!", reply_markup=get_buttons())

# ====== WHALE TRACKER ======
async def check_whale(context: ContextTypes.DEFAULT_TYPE):
    global last_block
    while True:
        try:
            current_block = w3.eth.block_number
            if current_block > last_block:
                # Add your whale tracking logic here
                print("New block:", current_block)
                last_block = current_block
            await asyncio.sleep(15)
        except Exception as e:
            print(f"Error in check_whale: {e}")
            await asyncio.sleep(30)

# ====== RUN BOT ======
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    
    # This runs check_whale every 15 seconds
    app.job_queue.run_repeating(check_whale, interval=15, first=5)

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
