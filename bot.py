import os
import requests
import time
import threading
from telethon import TelegramClient, events, Button

TELEGRAM_TOKEN = "8794247085:AAEFQ0GXpFs4fEAhiuogT2G-6uraiF6aSYA"
BSC_API_KEY = "5IHURITE5X1Y7543YIHA7YMTBFP8PZF69P"
MASTER_WALLET = "0x822c562a19317e9c61269C0Fdab90E48AA43Fc6F" # <-- CHANGE THIS TO 0x WALLET YOU WANT TO COPY

api_id = 30956794
api_hash = "ab6d89c900dd83ac83170c088c8e3380" # <-- YOUR API HASH ADDED

client = TelegramClient('bot', api_id, api_hash).start(bot_token=TELEGRAM_TOKEN)

SUBSCRIBERS = set()
LAST_TX = None
def get_balance(wallet):
    try:
        url = f'https://api.bscscan.com/api?module=account&action=balance&address={wallet}&tag=latest&apikey={BSC_API_KEY}'
        r = requests.get(url).json()
        balance = int(r['result']) / 10**18
        return balance
    except:
        return 0

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    buttons = [
        [Button.inline('💰 Balance', 'balance'), Button.inline('📡 Copy Trade', 'copytrade')],
        [Button.inline('⚡ Buy', 'buy'), Button.inline('🔥 Sell', 'sell')],
        [Button.inline('❓ Help', 'help')]
    ]
    await event.respond("**Ahmad DEX Bot**\nChoose an option:", buttons=buttons)

@client.on(events.CallbackQuery)
async def handler(event):
    data = event.data.decode('utf-8')
    if data == 'balance':
        bal = get_balance(MASTER_WALLET)
        await event.answer(f"💰 Master Balance: {bal:.4f} BNB", alert=True)
    elif data == 'copytrade':
        SUBSCRIBERS.add(event.sender_id)
        await event.answer("✅ You are subscribed to Copy Trade!", alert=True)
    elif data == 'buy':
        await event.answer("Send: /buy TOKEN_ADDRESS AMOUNT", alert=True)
    elif data == 'sell':
        await event.answer("Send: /sell TOKEN_ADDRESS %", alert=True)
    elif data == 'help':
        await event.answer("Commands: /start /balance /copytrade", alert=True)
@client.on(events.NewMessage(pattern=r'/buy (.+)'))
async def buy_handler(event):
    token = event.pattern_match.group(1)
    await event.respond(f'🟡 Buying {token}\n\nNote: This is demo mode. Real trading needs private key + web3')

@client.on(events.NewMessage(pattern=r'/sell (.+)'))
async def sell_handler(event):
    token = event.pattern_match.group(1)
    await event.respond(f'🔴 Selling {token}\n\nNote: This is demo mode. Real trading needs private key + web3')

client.start()
client.run_until_disconnected()
def watch_wallet():
    global LAST_TX
    print('Watching for trades...')
    while True:
        try:
            url = f'https://api.bscscan.com/api?module=account&action=txlist&address={MASTER_WALLET}&startblock=0&endblock=999&sort=desc&apikey={BSC_API_KEY}'
            r = requests.get(url).json()
            if r['status'] == '1' and r['result']:
                txs = r['result']
                if txs[0]['hash']!= LAST_TX:
                    LAST_TX = txs[0]['hash']
                    value = int(txs[0]['value']) / 10**18
                    to_addr = txs[0]["to"]
                    msg = f'🚨 **MASTER TRADE DETECTED** 🚨\n\nValue: {value:.4f} BNB\nTo: `{to_addr}`\nTx: https://bscscan.com/tx/{LAST_TX}'
                    for user in SUBSCRIBERS:
                        client.loop.create_task(client.send_message(user, msg))
            time.sleep(15)
        except Exception as e:
            print("Error:", e)
            time.sleep(15)

threading.Thread(target=watch_wallet, daemon=True).start()
print('DEX CopyBot started and watching your wallet')
client.run_until_disconnected()
