from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import telegram
import openai
from moviepy.editor import AudioFileClip
import concurrent.futures

openai.api_key = "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"
TELEGRAM_API_TOKEN = "6571312426:AAH5pw506xnRgAaaK4NuhXZXj_AB9gBre3c"

# Multilingual description
description_punjabi = "ਕ੍ਰਿਸ਼ੀ ਸਹਾਇਕ ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ!\n" \
                      "ਇਹ ਬੋਟ ਦੁਨੀਆ ਭਰ ਦੇ ਕਿਸਾਨਾਂ ਨੂੰ ਸਹਾਇਤਾ ਅਤੇ ਮਾਰਗ ਦਰਸ਼ਨ ਪ੍ਰਦਾਨ ਕਰਨ ਲਈ ਹੈ। " \
                      "ਇਹ ਫਸਲਾਂ ਦੀਆਂ ਬਿਮਾਰੀਆਂ ਅਤੇ ਨਦੀਨਾਂ ਦੀ ਰੋਕਥਾਮ ਵਾਲੇ ਕਿਸਾਨਾਂ ਨੂੰ ਬਾਗਬਾਨੀ ਅਤੇ ਹੋਰ ਸਵਾਲਾਂ ਵਿੱਚ ਮਦਦ ਕਰ ਸਕਦਾ ਹੈ। " \
                      "ਇਹ ਉਤਪਾਦਕਤਾ ਨੂੰ ਵਧਾਉਣ ਅਤੇ ਟਿਕਾਊ ਵਿਕਾਸ ਨੂੰ ਉਤਸ਼ਾਹਤ ਕਰਨ 'ਤੇ ਵੀ ਕੇਂਦ੍ਰਤ ਕਰਦਾ ਹੈ। " \
                      "ਖੇਤੀ ਨਾਲ ਸਬੰਧਿਤ ਕੋਈ ਵੀ ਸਵਾਲ ਪੁੱਛਣ ਲਈ ਬੇਝਿਜਕ ਮਹਿਸੂਸ ਕਰੋ, ਅਤੇ ਬੋਟ ਮਦਦਗਾਰੀ ਸਲਾਹ ਅਤੇ ਜਾਣਕਾਰੀ ਪ੍ਰਦਾਨ ਕਰਨ ਲਈ ਆਪਣੀ ਪੂਰੀ ਕੋਸ਼ਿਸ਼ ਕਰੇਗਾ।"

description_english = "Welcome to the AI Agricultural Assistant!\n" \
                      "This bot is here to offer valuable support and guidance to farmers around the world. " \
                      "It can help with everything from crop diseases and weed control to plantation and other farming queries, " \
                      "all while focusing on improving productivity and promoting sustainable practices. " \
                      "Feel free to ask any farming-related questions, and the bot will do its best to provide helpful advice and information."

description_hindi = "कृषि सहायक में आपका स्वागत है!\n" \
                    "यह बॉट दुनिया भर के किसानों को समर्थन और मार्गदर्शन प्रदान करने के लिए है। " \
                    "यह किसानों को फसल के रोगों और खरपतवार नियंत्रण से लेकर बागवानी और अन्य खेती संबंधित सवालों में मदद कर सकता है, " \
                    "साथ ही उत्पादकता को बढ़ाने और सतत अभिवृद्धि को प्रोत्साहित करने पर ध्यान केंद्रित करता है। " \
                    "खेती से संबंधित किसी भी प्रश्न को पूछने के लिए स्वतंत्र महसूस करें, और बॉट सहायक सलाह और जानकारी प्रदान करने के लिए अपनी पूरी कोशिश करेगा।"

description_multilingual = f"{description_punjabi}\n\n{description_english}\n\n{description_hindi}"

# Instruction Message
instruction_message = {
    "role": "system",
    "content": "You are only a farming and agricultural themed assistant bot. Do not answer any question about any place or any other thing except farming and agriculture themed questions. Be very creative, friendly at all times and especially while greeting, greet with new responses everytime. It's my strict order to Don't ever answer questions/query other than farming and agriculture themed. If a user asks queries other than farming and agriculture theme, then deny in a polite manner."
}

messages = [instruction_message]

# Rest of your code...

def get_assistant_response(messages, temperature=0.8):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature
    )
    return response["choices"][0]["message"]["content"]

def send_instruction_message(messages):
    messages.append(instruction_message)
    response = get_assistant_response(messages)
    messages.pop()  # Remove the instruction message from the message list
    return response

def text_message(update, context):
    messages.append({"role": "user", "content": update.message.text})

    # Send the instruction message as a reminder before generating the response
    instruction_response = send_instruction_message(messages)

    # Get the actual response
    response = get_assistant_response(messages)

    update.message.reply_text(text=f"** {response}", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "assistant", "content": response})

def voice_message(update, context):
    update.message.reply_text("I've received your voice message! Please give me a second to respond :)")
    voice_file = context.bot.getFile(update.message.voice.file_id)
    voice_file.download("voice_message.ogg")
    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")
    audio_file = open("voice_message.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file).text
    update.message.reply_text(text=f"*You :* _{transcript}_", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "user", "content": transcript})

    # Send the instruction message as a reminder before generating the response
    instruction_response = send_instruction_message(messages)

    # Get the actual response
    response = get_assistant_response(messages)

    update.message.reply_text(text=f"** {response}", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "assistant", "content": response})

def process_concurrent_tasks():
    # Perform other data processing tasks here (if any) that can be done concurrently
    pass

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=description_multilingual)

def start_bot():
    updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), text_message))
    dispatcher.add_handler(MessageHandler(Filters.voice, voice_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    start_bot()