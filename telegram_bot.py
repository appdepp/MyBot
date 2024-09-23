import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# Ваш токен бота
TOKEN = '8183641238:AAFCkwm9ovfRoZ2LsPSWyGG3O30sENgAo-k'

# Погода через OpenWeather API
API_KEY = '29b7ad9aecc4a023c3a2601e3242b851'


# Стартовое сообщение
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Выберите как получить текущую погоду: отправьте свою геолокацию или напишите название города.",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Отправить геолокацию", request_location=True)],
                [KeyboardButton("Ввести город")]
            ],
            one_time_keyboard=True
        ))


# Обработчик геолокации
async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_location = update.message.location
    weather_info = get_current_weather_by_coordinates(user_location.latitude, user_location.longitude)
    await update.message.reply_text(f"Текущая погода для вашей геолокации:\n{weather_info}")


# Обработчик ввода города
async def city_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city_name = update.message.text
    if city_name.lower() != "ввести город":
        weather_info = get_current_weather_by_city(city_name)
        await update.message.reply_text(f"Текущая погода для города {city_name}:\n{weather_info}")
    else:
        await update.message.reply_text("Пожалуйста, введите название города.")


# Получение текущей погоды по координатам
def get_current_weather_by_coordinates(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Ошибка при запросе: {response.status_code}, {response.text}")
        return "Ошибка получения текущей погоды."

    data = response.json()

    if 'main' not in data:
        return "Ошибка получения текущей погоды."

    temp = data['main']['temp']
    weather_description = data['weather'][0]['description']

    return f"{temp}°C, {weather_description}"


# Получение текущей погоды по названию города
def get_current_weather_by_city(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Ошибка при запросе: {response.status_code}, {response.text}")
        return "Ошибка получения текущей погоды для города."

    data = response.json()

    if 'main' not in data:
        return "Ошибка получения текущей погоды для города."

    lat = data['coord']['lat']
    lon = data['coord']['lon']

    # Используем координаты города для получения текущей погоды
    return get_current_weather_by_coordinates(lat, lon)


# Основная функция для запуска бота
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.LOCATION, location_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, city_weather))

    # Запускаем polling
    application.run_polling()


# Запускаем бота
if __name__ == '__main__':
    main()