from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils import executor
import aiohttp

API_TOKEN = "7919927542:AAHIpxOX7USztgxgqK5H9_WHYEp6hgjTtlQ"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

WEB_APP_URL = "https://ВАШ_ДОМЕН/webapp"  # Укажите ссылку на ваш хостинг с фронтендом

@dp.message_handler(commands="start")
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    web_app_button = InlineKeyboardButton(text="Открыть Web App", web_app=WebAppInfo(url=WEB_APP_URL))
    keyboard.add(web_app_button)
    await message.answer("Добро пожаловать! Нажмите на кнопку ниже, чтобы открыть Web App.", reply_markup=keyboard)

@dp.message_handler(commands="price")
async def get_crypto_price(message: types.Message):
    args = message.text.split()
    if len(args) < 3:
        await message.reply("Формат: /price <количество> <валюта> <целевая валюта>\nПример: /price 1 btc usd")
        return
    
    amount, from_currency, to_currency = args[1], args[2].upper(), args[3].upper()
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.coingecko.com/api/v3/simple/price?ids={from_currency}&vs_currencies={to_currency}") as response:
            data = await response.json()
            if from_currency in data and to_currency in data[from_currency]:
                price = data[from_currency][to_currency]
                total_price = float(amount) * price
                await message.reply(f"{amount} {from_currency} ≈ {total_price} {to_currency}")
            else:
                await message.reply("Не удалось получить цену. Проверьте валюту.")
