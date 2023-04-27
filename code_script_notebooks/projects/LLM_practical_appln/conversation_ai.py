import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

from langchain.llms import OpenAI
from langchain import OpenAI, LLMMathChain

import os
os.environ['OPENAI_API_KEY']='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'

from langchain import PromptTemplate, OpenAI, LLMChain

llm = OpenAI(temperature=0)

llm_math = LLMMathChain(llm=llm,
                        verbose=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and introduces itself."""

    await context.bot.send_message(chat_id=update.effective_chat.id,
        text="""Hi! My name is Math Professor. I will hold a math conversation with you.
        Send /cancel to stop talking to me.\n\n""")


async def bot_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns the reply to user after getting reply from server."""
    user = update.message.from_user
    logger.info("Question from User: %s", update.message.text)
    if update.message.text != '':
        llm_reply = llm_math.run(update.message.text)
    else:
        return 

    await update.message.reply_text(llm_reply)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day."
    )

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("token").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,bot_reply))
    application.add_handler(CommandHandler("cancel", cancel))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
