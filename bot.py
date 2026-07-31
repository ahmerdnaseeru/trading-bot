import os
from telethon import TelegramClient, events, Button

API_ID = int(os.getenv("API_ID"))          
API_HASH = os.getenv("API_HASH")           
BOT_TOKEN = os.getenv("BOT_TOKEN")         

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

GC_LINK = "https://t.me/dextradinggc"  # <-- YOUR GROUP LINK

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    buttons = [
        [Button.inline('Balance', b'balance'), Button.inline('Copy Trade', b'copytrade')],
        [Button.inline('Buy', b'buy'), Button.inline('Sell', b'sell')],
        [Button.url('📢 TG Group', GC_LINK)]
    ]
    await event.respond(f'**Ahmad DEX Bot**\nWelcome! Choose an option:', buttons=buttons)

@client.on(events.CallbackQuery(data=b'buy'))
async def buy(event):
    await event.respond("Buy feature coming soon")

@client.on(events.CallbackQuery(data=b'sell'))
async def sell(event):
    await event.respond("Sell feature coming soon")

@client.on(events.CallbackQuery(data=b'balance'))
async def balance(event):
    await event.respond("Balance: 0 BNB\nWallet: Demo")

@client.on(events.CallbackQuery(data=b'copytrade'))
async def copytrade(event):
    await event.respond("Copy Trade feature coming soon")

print("Bot with TG Group + Copy Trade starting...")
client.run_until_disconnected()
