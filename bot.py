import os
import asyncio
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ====== LOAD SECRETS ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ====== BACKUP RPCs ======
RPC_LIST = [
    "https://bsc-dataseed.binance.org/",
    "https://bsc-rpc.publicnode.com",
    "https://rpc.ankr.com/bsc"
]
BSC_RPC = None
last_block = 0

print("Connecting to BSC...")
for rpc in RPC_LIST:
    try:
        r = requests.post(rpc, json={"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}, timeout=5)
        last_block = int(r.json()['result'], 16)
        BSC_RPC = rpc
        print(f"Connected to BSC! Block: {last_block} via {rpc}")
        break
    except:
        print(f"Failed: {rpc}")
        continue

if BSC_RPC is None:
    print("ERROR: All RPCs failed")
    exit()

WHALE_WALLET = "0xYOUR_WALLET_ADDRESS_HERE"  # <-- CHANGE THIS TO YOUR WALLET
KOMA_CONTRACT = "0x55d398326f99059fF775485246999027B3197955"

def get_buttons():
    keyboard = [
        [InlineKeyboardButton("📊 Chart", url=f"https://poocoin.app/tokens/{KOMA_CONTRACT}")],
        [InlineKeyboardButton("💎 Buy", url=f"https://pancakeswap.finance/swap?outputCurrency={KOMA_CONTRACT}")],
        [InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🚀 *KOMA Whale Bot is LIVE* 🚀\n\nWatching: `{WHALE_WALLET[:10]}...`\nRPC: `{BSC_RPC}`",
        reply_markup=get_buttons(),
        parse_mode="Markdown"
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "refresh":
        await query.edit_message_text("🔄 Refreshed!", reply_markup=get_buttons())

async def check_whale(app):
    global last_block
    while True:
        try:
            r = requests.post(BSC_RPC, json={"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}, timeout=10)
            current_block = int(r.json()['result'], 16)
            if current_block > last_block:
                print(f"New block: {current_block}")
                last_block = current_block
            await asyncio.sleep(10)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(20)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    
    # Start whale checker
    asyncio.create_task(check_whale(app))
    
    print("Bot is running...")
    await app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    asyncio.run(main())
