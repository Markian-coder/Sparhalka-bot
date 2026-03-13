import telebot
import wikipedia

TOKEN = "8518097234:AAFcMWJgfbwcfH2QKer3qFGg-wI7mvlIgVw"
bot = telebot.TeleBot(TOKEN)

wikipedia.set_lang("uk")


user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Йо 😎 Напиши мені тему — я зроблю міні-шпаргалку з Вікіпедії!\n"
        "Щоб отримати ще 2 речення, пиши 'ще'"
    )

@bot.message_handler(content_types=['text'])
def wiki_short(message):
    chat_id = message.chat.id
    text = message.text.strip()

    # Якщо юзер пише "ще"
    if text.lower() == "ще":
        if chat_id not in user_data:
            bot.send_message(chat_id, "⚠ Спочатку напиши тему")
            return

        topic, sentences, index = user_data[chat_id]
        if index >= len(sentences):
            bot.send_message(chat_id, "🎉 Більше речень нема")
            return

        snippet = ". ".join(sentences[index:index+2]) + "."
        user_data[chat_id] = (topic, sentences, index+2)  # оновлюємо прогрес
        bot.send_message(chat_id, snippet)
        return

    # Якщо нова тема
    try:
        page = wikipedia.page(text)
        content = page.content
        sentences = content.split(". ")

        snippet = ". ".join(sentences[:2]) + "."

        # Беремо перші 2 зображення, якщо є
        images = [img for img in page.images if img.lower().endswith(('.jpg', '.jpeg', '.png'))][:2]

        # Зберігаємо тему та прогрес (без фоток, бо вони тільки при старті)
        user_data[chat_id] = (text, sentences, 2)

        # Відправляємо перший шматок тексту
        bot.send_message(chat_id, snippet)

        # Відправляємо фото тільки при першому запиті
        for img in images:
            bot.send_photo(chat_id, img)

    except wikipedia.exceptions.DisambiguationError as e:
        bot.send_message(chat_id, f"⚠ Тема неоднозначна, уточни: {e.options[:5]}")
    except wikipedia.exceptions.PageError:
        bot.send_message(chat_id, "❌ Такої сторінки нема")
    except Exception as e:
        bot.send_message(chat_id, f"Щось пішло не так 😅\n{e}")

bot.polling(none_stop=True)



