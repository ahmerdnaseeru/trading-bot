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
KOMA_CONTRACT = "0x55d398326f99059fF775485246999027B3197955"  # USDT
WHALE_WALLET = "0xYOUR_WALLET_ADDRESS_HERE"    # <-- PUT YOUR WALLET HERE

w3 = Web3(Web3.HTTPProvider(BSC_RPC))
last_block = w3.eth.block_number

# ====== BUTTONS ======
def get_buttons():
    keyboard = [
        [InlineKeyboardButton("📊 Chart", url=f"https://poocoin.app/tokens/{KOMA_CONTRACT}")],
        [InlineKeyboardButton("💎 Buy USDT", url=f"https://pancakeswap.finance/swap?outputCurrency={KOMA_CONTRACT}")],
        [InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== COMMANDS ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 *KOMA Whale Bot is LIVE* 🚀\n\nWatching wallet: " + WHALE_WALLET[:10] + "...",
        reply_markup=get_buttons(),
        parse_mode="Markdown"
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "refresh":
        await query.edit_message_text("🔄 Refreshed!", reply_markup=get_buttons())

# ====== WHALE TRACKER ======
async def whale_loop(app):
    global last_block
    while True:
        try:
            current_block = w3.eth.block_number
            if current_block > last_block:
                print("New block:", current_block)
                last_block = current_block
            await asyncio.sleep(15)
        except Exception as e:
            print(f"Error in whale_loop: {e}")
            await asyncio.sleep(30)

# ====== RUN BOT ======
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    
    # Start whale loop in background
    asyncio.create_task(whale_loop(app))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
