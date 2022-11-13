import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ContentType
from aiogram.utils.callback_data import CallbackData

bot = Bot(token = "YOUR_TELEGRAM_BOT_TOKEN")
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup()
    press_btn = types.InlineKeyboardButton("Bot Info",callback_data="press")
    keyboard_markup.row(press_btn)
    await message.reply("Text me the city and I'll send you the weather", reply_markup=keyboard_markup)

@dp.message_handler()   
async def get_weather(message: types.Message):   
    try:
        open_weather_token = "YOUR_OPEN_WEATHER_TOKEN"
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        
        def get_advice(temp):
            if temp < -10:
                return "It's very cold outside. Dress in your warmest clothes"
            elif temp < 0:
                return "It's pretty cold outside. We recommend that you wear anything warm"
            elif temp < 10:
                return "It's cold outside. Dress warmly"
            elif temp < 20:
                return "It's chilly outside, so dress warmer."
            elif temp < 25:
                return "It's pretty warm outside. However, I recommend that you wear a sweatshirt"
            elif temp < 30:
                return "It's warm outside. You can walk around in a T-shirt"
            elif temp < 35:
                return "It's hot outside. Dress loosely"
            else:
                return "It's very hot outside. Be careful in this heat"
            
        
        name = data["name"]
        temp = data["main"]["temp"]
        feelslike = data["main"]["feels_like"]
        description = data["weather"][0]["main"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        
        
        await message.reply(f"*City*: {name}\n*Temperature*: {temp} °C, but feels like {feelslike} °C\n"
              f"*Humidity*: {humidity}\n*Pressure*: {pressure}\n"
              f"*Wind*: {wind}\n*Description*: {description}\n"
              f"*{get_advice(temp)}*",parse_mode="Markdown")
        
    except Exception as ex:
        
        await message.reply("Check your city name")
@dp.callback_query_handler(lambda c: c.data == 'press')
async def about_bot_message(call: types.CallbackQuery):
    await call.answer("Hello. I'm Weather bot. I was created to find weather information for you.", True)
      
@dp.message_handler(content_types=ContentType.ANY)
async def answer_on_foto(message: types.Message):
    content_types = ContentType.TEXT
    await message.reply("*I don't know what you mean. Please text the city!*",parse_mode="Markdown")

if __name__ == '__main__':
    executor.start_polling(dp)