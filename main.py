from typing import Final
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print('Starting up bot...')

TOKEN: Final = '6285294967:AAEduEmS7rG8TrNCEV2OWHEEqAe0JAUg_WU'
BOT_USERNAME: Final = '@voiceeapp_bot'
USERS_QUESTIONS = {}
USERS_PODCASTS = {}
bot = Bot(TOKEN)
ADMINS = [462048028,  585363683]


# System functions
# Функция для чтения данных из файла podcasts.txt
def read_podcasts_from_file():
    try:
        with open('podcasts.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                user_id, message_id, message = line.strip().split(',')
                user_id = int(user_id)
                message_id = int(message_id)
                if user_id in USERS_PODCASTS:
                    USERS_PODCASTS[user_id][message_id] = message
                else:
                    USERS_PODCASTS[user_id] = {message_id: message}

        print('Podcasts data loaded from file.')
    except FileNotFoundError:
        print('Podcasts file not found. Creating a new file.')


# Функция для чтения данных из файла questions.txt
def read_questions_from_file():
    try:
        with open('questions.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                user_id, message_id, message = line.strip().split(',')
                user_id = int(user_id)
                message_id = int(message_id)
                if user_id in USERS_QUESTIONS:
                    USERS_QUESTIONS[user_id][message_id] = message
                else:
                    USERS_QUESTIONS[user_id] = {message_id: message}

        print('Questions data loaded from file.')
    except FileNotFoundError:
        print('Questions file not found. Creating a new file.')


# Функция для записи данных в файл podcasts.txt
def write_podcasts_to_file():
    with open('podcasts.txt', 'w') as f:
        for user_id, messages in USERS_PODCASTS.items():
            for message_id, message in messages.items():
                line = f"{user_id},{message_id},{message}\n"
                f.write(line)

    print('Podcasts data saved to file.')


# Функция для записи данных в файл questions.txt
def write_questions_to_file():
    with open('questions.txt', 'w') as f:
        for user_id, messages in USERS_QUESTIONS.items():
            for message_id, message in messages.items():
                line = f"{user_id},{message_id},{message}\n"
                f.write(line)

    print('Questions data saved to file.')


# User commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я бот VoiceApp, Я могу Вам помочь с отправкой подкастов или ответить на '
                                    'интерисующие Вас вопросы')
    context.user_data['prev_command'] = 'start'


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, введите Ваш вопрос")
    context.user_data['prev_command'] = 'help'


async def podcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, пришлите ваш подкаст в виде аудио сообщения или mp3 файла")
    context.user_data['prev_command'] = 'podcast'


# Admin commands
async def show_questions_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in ADMINS:
        outp = ""
        print(USERS_QUESTIONS)
        if len(USERS_QUESTIONS) != 0:
            for user_id, messages in USERS_QUESTIONS.items():
                for message_id, message in messages.items():
                    outp += 'ID пользователя и ID сообщения: ' + str(user_id) + ' ' + str(
                        message_id) + '\nВопрос: ' + message + "\n"
                    outp += '\n'
            await update.message.reply_text(outp)
        else:
            await update.message.reply_text('Вопросов нет :)')
    else:
        await update.message.reply_text("Комманда только для администратора")
    context.user_data['prev_command'] = 'admin_show_q'


async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in ADMINS:
        outp = ""
        print(USERS_QUESTIONS)
        if len(USERS_QUESTIONS) != 0:
            for user_id, messages in USERS_QUESTIONS.items():
                for message_id, message in messages.items():
                    outp += 'ID пользователя и ID сообщения: ' + str(user_id) + ' ' + str(
                        message_id) + '\nВопрос: ' + message + "\n"
                    outp += '\n'
            await update.message.reply_text(outp)
            await update.message.reply_text("Введите ID пользователя, ID сообщения и текст ответа")
        else:
            await update.message.reply_text('Вопросов нет :)')
    else:
        await update.message.reply_text("Комманда только для администратора")
    context.user_data['prev_command'] = 'admin_answ_q'


async def show_podcasts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in ADMINS:
        print(USERS_PODCASTS)
        if len(USERS_PODCASTS) != 0:
            await bot.sendMessage(chat_id=user.id, text='Подкасты на рассмотрении:')
            for user_id, messages in USERS_PODCASTS.items():
                for message_id, message in messages.items():
                    outp = 'ID пользователя и ID сообщения: ' + str(user_id) + ' ' + str(
                        message_id) + '\nИмя: ' + message
                    await bot.sendMessage(chat_id=user.id, text=outp)
                    await bot.forward_message(chat_id=user.id, from_chat_id=user_id, message_id=message_id)
        else:
            await update.message.reply_text('Подкастов нет :(')
    else:
        await update.message.reply_text("Комманда только для администратора")
    context.user_data['prev_command'] = 'admin_show_p'


async def answer_podcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in ADMINS:
        print(USERS_PODCASTS)
        if len(USERS_PODCASTS) != 0:
            await bot.sendMessage(chat_id=user.id, text='Подкасты на рассмотрении:')
            for user_id, messages in USERS_PODCASTS.items():
                for message_id, message in messages.items():
                    outp = 'ID пользователя и ID сообщения: ' + str(user_id) + ' ' + str(
                        message_id) + '\nИмя: ' + message
                    await bot.sendMessage(chat_id=user.id, text=outp)
                    await bot.forward_message(chat_id=user.id, from_chat_id=user_id, message_id=message_id)
        else:
            await update.message.reply_text('Подкастов нет :(')
        await update.message.reply_text("Введите ID пользователя, ID сообщения и Y для одобрения"
                                        "\nПример: 1111111111 123 Y"
                                        "\n\nЕсли подкаст не прошел модерацию, то опишите причину. Она будет отправлена пользователю"
                                        "\nПример: 1111111111 123 Маты это плохо")
    else:
        await update.message.reply_text("Комманда только для администратора")
    context.user_data['prev_command'] = 'admin_answ_p'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    async def handle_help_command():
        user = update.effective_user
        message_id = update.message.message_id
        user_question = user.first_name + ' ' + user.last_name + ' ' + text
        if user.id in USERS_QUESTIONS:
            USERS_QUESTIONS[int(user.id)][int(message_id)] = user_question
        else:
            USERS_QUESTIONS[int(user.id)] = {int(message_id): user_question}
        write_questions_to_file()
        await update.message.reply_text(f"{user.first_name}, Мы получили Ваше сообщение. Администратор скоро свяжется "
                                        f"с Вами")
        context.user_data['prev_command'] = 'default'
        print(USERS_QUESTIONS)

    async def handle_admin_answ_command():
        parts = text.split()
        user_id = parts[0]
        message_id = parts[1]
        answer = ' '.join(parts[2:])
        print(user_id, message_id, answer)
        if user_id and message_id:
            if int(user_id) in USERS_QUESTIONS.keys():
                if int(message_id) in USERS_QUESTIONS[int(user_id)]:
                    if answer:
                        await bot.sendMessage(chat_id=user_id, text=answer, reply_to_message_id=int(message_id))
                    else:
                        await update.message.reply_text('Вы забыли ввести ответ! Перезапустите команду-ответ')
                    del USERS_QUESTIONS[int(user_id)][int(message_id)]
                    if USERS_QUESTIONS[int(user_id)] == {}:
                        del USERS_QUESTIONS[int(user_id)]
                    write_questions_to_file()
        context.user_data['prev_command'] = 'default'

    async def handle_podcast_command():
        message = update.message
        user = update.effective_user
        message_id = update.message.message_id
        print(message.document)
        if message.voice or (message.document and message.document.mime_type == 'audio/mpeg'):
            if user.id in USERS_PODCASTS:
                USERS_PODCASTS[int(user.id)][int(message_id)] = str(user.first_name + ' ' + user.last_name)
            else:
                USERS_PODCASTS[int(user.id)] = {int(message_id): str(user.first_name + ' ' + user.last_name)}
            await update.message.reply_text(
                f"{user.first_name}, Мы получили Ваш подкаст. Администраторы скоро проверят подкаст и свяжутся с Вами")
            write_podcasts_to_file()
        else:
            await update.message.reply_text(f"{user.first_name}, просим прощения, но мы не получили Ваш подкаст. "
                                            f"Пожалуйста, удостоверьтесь, что ваше сообщение содержит mp3 файл "
                                            f"или аудиосообщение без текста в сообщении. "
                                            f"Пожалуйста, введите команду еще раз")
        context.user_data['prev_command'] = 'default'

    async def handle_answer_podcast_command():
        parts = text.split()
        user_id = parts[0]
        message_id = parts[1]
        answer = ' '.join(parts[2:])
        print(user_id, message_id, answer)
        if answer.lower() == 'y':
            if user_id and message_id:
                if int(user_id) in USERS_PODCASTS.keys():
                    if int(message_id) in USERS_PODCASTS[int(user_id)]:
                        await bot.sendMessage(chat_id=user_id, text='Ваш подкаст принят! Ожидайте публикации',
                                              reply_to_message_id=int(message_id))
            del USERS_PODCASTS[int(user_id)][int(message_id)]
            if USERS_PODCASTS[int(user_id)] == {}:
                del USERS_PODCASTS[user_id]
            write_podcasts_to_file()
        else:
            if user_id and message_id:
                if int(user_id) in USERS_PODCASTS.keys():
                    if int(message_id) in USERS_PODCASTS[int(user_id)]:
                        await bot.sendMessage(chat_id=user_id, text=('Ваш подкаст отклонен! Причина: ' + answer),
                                              reply_to_message_id=int(message_id))
            del USERS_PODCASTS[int(user_id)][int(message_id)]
            write_podcasts_to_file()

        context.user_data['prev_command'] = 'default'

    async def handle_start_command():
        await update.message.reply_text("Пожалуйста, воспользуйтесь командами. Команды должны начинаться с символа /")

    async def handle_default_command():
        await update.message.reply_text("Извините, я Вас не понимаю. Пожалуйста, пользуйтесь командами")

    async def handle_unknown_command():
        await update.message.reply_text("SONOVA BITCH. HOOORI SHEIIIIIT. OH MAH GAAAAAAD")

    # Handle commands based on the value of 'prev_command'
    prev_command = context.user_data['prev_command']

    if prev_command == 'help':
        await handle_help_command()
    elif prev_command == 'admin_answ_q':
        await handle_admin_answ_command()
    elif prev_command == 'admin_answ_p':
        await handle_answer_podcast_command()
    elif prev_command == 'podcast':
        await handle_podcast_command()
    elif prev_command == 'start':
        await handle_start_command()
    elif prev_command == 'default':
        await handle_default_command()
    else:
        await handle_unknown_command()

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    read_podcasts_from_file()
    read_questions_from_file()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('podcast', podcast_command))
    app.add_handler(CommandHandler('a_show_q', show_questions_command))
    app.add_handler(CommandHandler('a_answ_q', answer_question))
    app.add_handler(CommandHandler('a_show_p', show_podcasts_command))
    app.add_handler(CommandHandler('a_answ_p', answer_podcast))

    # Messages
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
