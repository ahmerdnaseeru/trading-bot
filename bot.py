import os
from telethon import TelegramClient, events, Button

API_ID = int(os.getenv("API_ID"))          
API_HASH = os.getenv("API_HASH")           
BOT_TOKEN = os.getenv("BOT_TOKEN")         

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

GC_LINK = "https://t.me/dextradinggc"

def get_buttons():
    return [
        [Button.inline('Balance', b'balance'), Button.inline('Copy Trade', b'copytrade')],
        [Button.inline('Buy', b'buy'), Button.inline('Sell', b'sell')],
        [Button.url('📢 TG Group', GC_LINK)]
    ]

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    buttons = get_buttons()
    await event.reply(f'**Ahmad DEX Bot**\nWelcome! Choose an option:', buttons=buttons)

@client.on(events.CallbackQuery)
async def handler(event):
    data = event.data.decode('utf-8')
    
    if data == 'buy':
        text = "Buy feature coming soon"
    elif data == 'sell':
        text = "Sell feature coming soon"
    elif data == 'balance':
        text = "Balance: 0 BNB\nWallet: Demo"
    elif data == 'copytrade':
        text = "Copy Trade feature coming soon"
    else:
        text = "Unknown"
    
    # This edits the current message instead of sending new one
    await event.edit(f'**Ahmad DEX Bot**\n{text}', buttons=get_buttons())

print("Bot starting with edit mode...")
client.run_until_disconnected()
