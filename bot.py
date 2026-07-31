import os
import asyncio
import requests
from web3 import Web3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
async def check_whale():
    global last_block
    while True:
        try:
            current_block = w3.eth.block_number
            for block_num in range(last_block + 1, current_block + 1):
                block = w3.eth.get_block(block_num, full_transactions=True)
                for tx in block.transactions:
                    if tx.to and tx.to.lower() == KOMA_CONTRACT:
                        if tx["from"].lower() == WHALE_WALLET:
                            amount_bnb = w3.from_wei(tx.value, 'ether')
                            msg = f"🐋 <b>KOMA WHALE BUY!</b>\nAmount: {amount_bnb} BNB\nTx: https://bscscan.com/tx/{tx.hash.hex()}"
                            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                            requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"})
            last_block = current_block
        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(10)


# ====== RUN BOT ======
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
asyncio.create_task(check_whale())
print("Bot is running...")
app.run_polling()

# ====== CONFIG ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BSC_RPC = os.getenv("BSC_RPC")
WHALE_WALLET = os.getenv("WHALE_WALLET", "0xB20f204A158e4E0DF40fA02B048BBbE2ea7ff3Cc8").lower()
KOMA_CONTRACT = os.getenv("KOMA_CONTRACT", "0xYOUR_KOMA_CONTRACT_ADDRESS_HERE").lower()

w3 = Web3(Web3.HTTPProvider(BSC_RPC))
last_block = w3.eth.block_number

# ====== BUTTONS ======
def get_buttons():
    keyboard = [
        [InlineKeyboardButton('💰 Balance', callback_data='balance')],
        [InlineKeyboardButton('🟢 Buy', callback_data='buy'), InlineKeyboardButton('🔴 Sell', callback_data='sell')],
        [InlineKeyboardButton('📢 TG Group', url="https://t.me/dextrading")]
    ]
    return InlineKeyboardMarkup(keyboard)


# ====== COMMANDS ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "**Ahmad DEX Bot - Live**\n\nConnected to BSC ✅\nWatching whale: `{}`\n\nChoose an option below:".format(WHALE_WALLET),
        reply_markup=get_buttons(),
        parse_mode='Markdown'
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'balance':
        await query.edit_message_text("Balance feature coming soon. Add WALLET_PRIVATE_KEY to check balance.")
    elif query.data == 'buy':
        await query.edit_message_text("Buy panel coming soon.")
    elif query.data == 'sell':
        await query.edit_message_text("Sell panel coming soon.")


# ====== WHALE CHECKER ======
async def check_whale():
    global last_block
    while True:
        try:
            current_block = w3.eth.block_number
            for block_num in range(last_block + 1, current_block + 1):
                block = w3.eth.get_block(block_num, full_transactions=True)
                for tx in block.transactions:
                    if tx.to and tx.to.lower() == KOMA_CONTRACT:
                        if tx["from"].lower() == WHALE_WALLET:
                            amount_bnb = w3.from_wei(tx.value, 'ether')
                            msg = f"🐋 <b>KOMA WHALE BUY!</b>\nAmount: {amount_bnb} BNB\nTx: https://bscscan.com/tx/{tx.hash.hex()}"
                            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                            requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"})
            last_block = current_block
        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(10)


# ====== RUN BOT ======
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

# Run whale checker in background
asyncio.create_task(check_whale())

print("Bot is running...")
app.run_polling()
