import telebot

bot = telebot.TeleBot('7537623107:AAEB2H3JPpWiTZeI6_GQ6InBjLfoliBV87E')

winners = {
    '2015–2016': 'Real Madrid',
    '2016–2017': 'Real Madrid',
    '2017–2018': 'Real Madrid',
    '2018–2019': 'Liverpool',
    '2019–2020': 'FC Bayern Munich',  # Исправлено на полное название
    '2020–2021': 'Chelsea',
    '2021–2022': 'Real Madrid',
    '2022–2023': 'Manchester City',
    '2023–2024': 'Real Madrid'
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который расскажет, выигрывала ли команда Лигу чемпионов УЕФА с сезона 2015–2016 по 2023–2024. Введи название команды!")

@bot.message_handler(content_types=['text'])
def handle_team(message):
    team = message.text.strip()
    response = f"Результаты для '{team}' в Лиге чемпионов УЕФА (2015–2024):\n\n"
    
    victories = [season for season, winner in winners.items() if team.lower() in winner.lower() or winner.lower() in team.lower()]
    victory_count = len(victories)
    
    if victory_count > 0:
        response += f"Команда '{team}' выигрывала Лигу чемпионов {victory_count} раз в период с сезона 2015–2016 по 2023–2024:\n"
        response += "\n".join([f"- {season}" for season in victories])
    else:
        response += f"Команда '{team}' не выигрывала Лигу чемпионов с сезона 2015–2016 по 2023–2024."

    bot.reply_to(message, response)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
