import datetime
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace 'YOUR_BOT_TOKEN' with your bot token from BotFather
TOKEN = '7909977759:AAEh2zT1R5CBp8jL0tTWqCdKPQwxe6A22tI'

# List of sample jokes
jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my computer I needed a break, and now it won't stop sending me Kit-Kats.",
    "Why was the math book sad? Because it had too many problems."
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I am your bot. Type /help to see what I can do.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Here are some commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Show available commands\n"
        "/weather - Get a sample weather report\n"
        "/time - Get the current time\n"
        "/calc <expression> - Calculate a mathematical expression\n"
        "/joke - Hear a random joke\n"
    )
    await update.message.reply_text(help_text)

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Sample response (for a real bot, connect to a weather API)
    await update.message.reply_text("Today's weather is sunny with a high of 25°C and a low of 15°C.")

async def time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"The current time is: {current_time}")

async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        expression = " ".join(context.args)  # Join the arguments to form the expression
        result = eval(expression)  # Evaluate the expression (be cautious with eval)
        await update.message.reply_text(f"The result of {expression} is {result}")
    except Exception as e:
        await update.message.reply_text("There was an error with your calculation. Please check your input.")

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    joke = random.choice(jokes)  # Select a random joke
    await update.message.reply_text(joke)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Echoes back whatever the user sends
    await update.message.reply_text(update.message.text)

def main():
    app = Application.builder().token(TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler("time", time))
    app.add_handler(CommandHandler("calc", calc))
    app.add_handler(CommandHandler("joke", joke))
    
    # Message handler to echo messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Run the bot
    app.run_polling()

if __name__ == '__main__':
    main()
