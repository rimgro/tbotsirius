from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import wiki

with open("tokenbt", "r") as ftb:
    TOKEN = ftb.readline().strip()

reply_keyboard = [["/address", "/phone"], ["/help"]]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

def echo(update, context):
    txt = update.message.text
    if txt.lower() in ['привет', 'здаров']:
        txt = "И тебе привет человек!"
    update.message.reply_text(txt)



def start(update, context):
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!"
    ,reply_markup=markup
    )

def close_keyboard(update, context):
    update.message.reply_text("ok", reply_markup=ReplyKeyboardRemove())


def help(update, context):
    update.message.reply_text(
        "/start - запуск бота\n/help - вызов помощи")

def address(update, context):
    update.message.reply_text("какой то адрес")

def phone(update, context):
    update.message.reply_text("какой то телефон")

def wikipedia(update, context):
    update.message.reply_text("Идет поиск в википедии...")
    print(context.args, " ".join(context.args), "=======")
    rezult, urlrez = wiki.search_wiki(" ".join(context.args))
    update.message.reply_text(rezult + urlrez)

def set_timer(update, context):
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text("Прошлое не вернуть :(")
            return
        if "job" in context.chat_data:
            old_job = context.chat_data["job"]
            old_job.schedule_removal()

        new_job = context.job_queue.run_repeating(task, due, context=chat_id)
        context.chat_data["job"] = new_job
        update.message.reply_text(f"Вернусь через {due} секунд")
    except(IndexError, ValueError):
        update.message.reply_text("Использование: /set <секунд>")


def task(context):
    job = context.job
    context.bot.send_message(job.context, text = "я вернулся")

def unset_timer(update, context):
    if "job" not in context.chat_data:
        update.message.reply_text("че надо")
        return

    old_job = context.chat_data["job"]
    old_job.schedule_removal()
    del context.chat_data["job"]
    update.message.reply_text("все, ладно, не вернусь")



def main():
    print("Бот запущен...")
    updater = Updater(TOKEN, use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Регистрируем обработчик в диспетчере.
    # обработка команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(CommandHandler("address", address))
    dp.add_handler(CommandHandler("wiki", wikipedia))
    dp.add_handler(CommandHandler("set", set_timer, pass_args=True, pass_job_queue=True,pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset_timer, pass_chat_data=True))
    # обработка сообщений
    dp.add_handler(MessageHandler(Filters.text, echo))
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
