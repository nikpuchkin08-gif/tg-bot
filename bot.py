import telebot
from telebot import types

TOKEN = "8626299706:AAFRZmzmqLoTU47LwFpCDB_JNg5p3z99k9c"


ADMIN_ID = 6607602685

bot = telebot.TeleBot(TOKEN)
user_data = {}

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("📝 Оставить заявку"))
    markup.row(types.KeyboardButton("📍 Адрес и контакты"), types.KeyboardButton("ℹ️ Услуги и цены"))
    return markup

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.send_message(
        message.chat.id,
        "👋 Здравствуйте! Выберите нужный раздел в меню ниже:",
        reply_markup=main_keyboard()
    )

@bot.message_handler(func=lambda msg: msg.text == "📍 Адрес и контакты")
def info_contacts(message):
    bot.send_message(
        message.chat.id,
        "📍 Наш адрес: ул. Красная, 100\n⏰ Работаем: 10:00 – 21:00\n📞 Телефон: +7 (999) 000-00-00"
    )

@bot.message_handler(func=lambda msg: msg.text == "ℹ️ Услуги и цены")
def info_services(message):
    bot.send_message(
        message.chat.id,
        "💈 Прайс-лист:\n— Услуга 1: 1 500 ₽\n— Услуга 2: 2 500 ₽\n— Комплекс: 3 500 ₽\n\nЧтобы записаться, нажмите «Оставить заявку»!"
    )

@bot.message_handler(func=lambda msg: msg.text == "📝 Оставить заявку")
def order_start(message):
    user_data[message.chat.id] = {}
    bot.send_message(
        message.chat.id,
        "Напишите, какая услуга или товар вас интересует?",
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, get_service)

def get_service(message):
    user_data[message.chat.id]['service'] = message.text
    bot.send_message(message.chat.id, "Отлично! Теперь напишите ваш контактный номер телефона для связи:")
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    user_data[message.chat.id]['phone'] = message.text
    data = user_data[message.chat.id]
    
    bot.send_message(
        message.chat.id,
        f"✅ Спасибо, {message.from_user.first_name}! Заявка принята. Менеджер свяжется с вами в ближайшее время.",
        reply_markup=main_keyboard()
    )
    
    admin_notification = (
        f"🔥 Новая заявка!\n\n"
        f"👤 Клиент: @{message.from_user.username or 'без_юзернейма'} ({message.from_user.first_name})\n"
        f"🛠 Интересует: {data['service']}\n"
        f"📞 Телефон: {data['phone']}"
    )
    bot.send_message(ADMIN_ID, admin_notification)

if __name__ == '__main__':
    print("Бот успешно запущен!")
    bot.infinity_polling(skip_pending=True)

