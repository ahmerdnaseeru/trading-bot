import os, asyncio
from telethon import TelegramClient, events, Button
from web3 import Web3

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BSC_RPC = os.getenv("BSC_RPC")

w3 = Web3(Web3.HTTPProvider(BSC_RPC)) # NOW CONNECTED TO BSC ✅

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def get_buttons():
    return [
        [Button.inline('💰 Balance', b'balance'), Button.inline('📡 Copy Trade', b'copytrade')],
        [Button.inline('🟢 Buy', b'buy'), Button.inline('🔴 Sell', b'sell')],
        [Button.url('📢 TG Group', "https://t.me/dextradinggc")] # YOUR GROUP IS STILL HERE
    ]

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply(
        '**Ahmad DEX Bot - Test Mode**\n\n'
        'Connected to BSC ✅\n'
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

print("Bot starting with BSC Connected + All Buttons...")
client.run_until_disconnected()
