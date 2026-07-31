import os
import asyncio
import requests
import time
from telethon import TelegramClient, events, Button
from web3 import Web3
from threading import Thread

# ====== YOUR CODES - HARDCODED FOR GITHUB ======
API_ID = 30956794  # <-- REPLACE with your API_ID
API_HASH = "ab6d89c900dd83ac83170c088c8e3380"  # <-- REPLACE with your API_HASH
BOT_TOKEN = "8794247085:AAEFQ0GXpFs4fEAhiuogT2G-6uraiF6aSYA"
TELEGRAM_CHAT_ID = "8826062913" # Your personal ID for whale alerts
BSC_RPC = "https://bsc-dataseed.binance.org/"
# ============================================

# ====== WHALE TRACKER CONFIG ======
KOMA_CONTRACT = "0xd5eaAaC47bD1993d661bc087E15dfb079a7f3C19"
WHALE_WALLET = "0xB20f204A158e4ED0F40fA02B048BbB2ea7ff3Cc8"
w3 = Web3(Web3.HTTPProvider(BSC_RPC))
last_block = w3.eth.block_number
# ==================================

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def get_buttons():
    return [
        [Button.inline('💰 Balance', b'balance'), Button.inline('📡 Copy Trade', b'copytrade')],
        [Button.inline('🟢 Buy', b'buy'), Button.inline('🔴 Sell', b'sell')],
        [Button.url('📢 TG Group', "https://t.me/dextradinggc")]
    ]

# ====== SEND TELEGRAM FUNCTION FOR ALERTS ======
def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"})
    except Exception as e:
        print(f"Telegram Error: {e}")

# ====== WHALE TRACKER BACKGROUND FUNCTION ======
def check_whale():
    global last_block
    while True:
        try:
            current_block = w3.eth.block_number
            for block_num in range(last_block + 1, current_block + 1):
                block = w3.eth.get_block(block_num, full_transactions=True)
                for tx in block.transactions:
                    if tx.to and tx.to.lower() == KOMA_CONTRACT.lower():
                        if tx["from"].lower() == WHALE_WALLET.lower():
                            amount_bnb = w3.from_wei(tx.value, 'ether')
                            msg = f"🚨 <b>KOMA WHALE BUY!</b> 🚨\n\n" \
                                  f"<b>Wallet:</b> <code>{WHALE_WALLET}</code>\n" \
                                  f"<b>Spent:</b> {amount_bnb} BNB\n" \
                                  f"<b>TX:</b> https://bscscan.com/tx/{tx.hash.hex()}"
                            send_telegram(msg)
            last_block = current_block
        except Exception as e:
            print(f"Whale Check Error: {e}")
        time.sleep(10)

def start_whale_watcher():
    send_telegram("✅ <b>Ahmad DEX Bot Started!</b>\n<b>KOMA Whale Watcher:</b> ACTIVE\nWatching: <code>0xB20f...3Cc8</code>")
    Thread(target=check_whale, daemon=True).start()
# ==============================================

# ====== YOUR OLD BOT COMMANDS ======
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply(
        '**Ahmad DEX Bot - Test Mode**\n\n'
        'Connected to BSC ✅\n'
        'Whale Tracker: ACTIVE 🚨\n\n'
        'Choose an option below:', 
        buttons=get_buttons()
    )

@client.on(events.CallbackQuery(data=b'balance'))
async def balance(event):
    await event.answer('Balance feature loading... Wallet connect coming next', alert=True)

@client.on(events.CallbackQuery(data=b'copytrade'))
async def copytrade(event):
    await event.edit(
        '**Copy Trade - Test Mode**\n'
        'Use: `/copy add <wallet_address>`\n\n'
        'Example: `/copy add 0x123...`', 
        buttons=get_buttons()
    )

@client.on(events.CallbackQuery(data=b'buy'))
async def buy(event):
    await event.answer('Buy feature coming in Real Mode', alert=True)

@client.on(events.CallbackQuery(data=b'sell'))
async def sell(event):
    await event.answer('Sell feature coming in Real Mode', alert=True)
# ===================================

async def main():
    # START WHALE WATCHER IN BACKGROUND
    await asyncio.to_thread(start_whale_watcher)
    print("Bot starting with BSC Connected + All Buttons + Whale Tracker...")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
