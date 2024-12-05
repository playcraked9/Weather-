import logging
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Enter your Telegram & Openweather API keys
TELEGRAM_API_KEY = "7752592653:AAFMlMeKKnEaO3L2HMB9fgQzSYTlMnx97Ts"
OPENWEATHERMAP_API_KEY = "2c7e072e1f1699166a8706253de3b6de"

def get_weather(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        city_name = data["name"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        weather_description = data["weather"][0]["description"]
        
        sunrise = datetime.utcfromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S')
        sunset = datetime.utcfromtimestamp(data["sys"]["sunset"]).strftime('%H:%M:%S')
        
        now = datetime.now()
        current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        return (
            f"📅 **Current Date and Time**: {current_date_time}\n\n"
            f"🌍 **Weather Report for {city_name}** 🌍\n"
            f"----------------------------------------\n"
            f"🌡 **Temperature**: {temperature}°C\n"
            f"🤗 **Feels Like**: {feels_like}°C\n"
            f"🌤 **Condition**: {weather_description.capitalize()}\n"
            f"💧 **Humidity**: {humidity}%\n"
            f"🌬 **Wind Speed**: {wind_speed} m/s\n"
            f"📊 **Pressure**: {pressure} hPa\n"
            f"🌅 **Sunrise**: {sunrise} UTC\n"
            f"🌇 **Sunset**: {sunset} UTC\n"
            f"----------------------------------------\n"
            f"✨ Stay safe and have a great day! ✨"
        )
    else:
        return "🚫 **City not found.** Please check the name and try again."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 **Welcome to the Weather Bot!** 🌤\n\n"
        "Use the command /weather `<city>` to get the current weather report.\n"
        "Example: `/weather New York`"
    )

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) == 0:
        await update.message.reply_text(
            "❗ **Please provide a city name.**\n"
            "Usage: `/weather <city>`\n"
            "Example: `/weather Paris`"
        )
        return
    
    city = " ".join(context.args)
    weather_report = get_weather(city)
    await update.message.reply_text(weather_report, parse_mode="Markdown")

def main():
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))

    logging.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
