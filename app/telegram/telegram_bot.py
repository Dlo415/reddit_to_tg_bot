from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os
from dotenv import load_dotenv
from app.reddit.reddit_api import RedditClient
import logging
# Basic configuration of the logging system
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from a .env file
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
user_agent = os.getenv('USER_AGENT')
bot_token = os.getenv('BOT_TOKEN')

class TelegramBot:
    """
    A Telegram bot class that interacts with Reddit API to fetch and send subreddit posts.
    """
    def __init__(self, bot_token, reddit_client):
        """
        Initializes the Telegram Bot with a bot token and a Reddit client instance.
        """
        self.bot_token = bot_token
        self.reddit_client = reddit_client
        self.application = Application.builder().token(bot_token).build()
        self.setup_handlers()
    def setup_handlers(self):
        """
        Sets up handlers for different bot commands.
        """
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CommandHandler('learnpython', self.send_subreddit_post))
        self.application.add_handler(CommandHandler('python', self.send_subreddit_post))
        self.application.add_handler(CommandHandler('learnprogramming', self.send_subreddit_post))
        self.application.add_handler(CommandHandler('qualityassurance', self.send_subreddit_post))
        self.application.add_handler(CommandHandler('cscareerquestions', self.send_subreddit_post))
        self.application.add_handler(CommandHandler('softwaretesting', self.send_subreddit_post))
        self.application.add_handler(CommandHandler('chatgpt', self.send_subreddit_post))

    async def start(self, update: Update, context: CallbackContext) -> None:
        """
        Handler for the /start command, sends a welcome message.
        """
        chat_id = update.effective_chat.id
        logger.info(f"User {update.effective_user.username} initiated the /start command.")
        await context.bot.send_message(chat_id=chat_id, text="Hello! I am your bot")

    async def send_subreddit_post(self, update: Update, context: CallbackContext) -> None:
        """
        Fetches and sends the most popular post from a given subreddit.
        """
        subreddit = update.message.text.lstrip('/') # Extract the subreddit name from the command text
        try:
            logger.info(f"Fetching posts from subreddit: {subreddit}")
            posts = self.reddit_client.get_20_new_posts(subreddit)
            most_popular_post = RedditClient.find_most_popular_post(posts)
            if not most_popular_post:
                logger.warning("No posts available in the subreddit.")
                await context.bot.send_message(chat_id=update.effective_chat.id, text="No posts available")
                return
            # Forming and sending the message
            message = (
                f"*Title:* {most_popular_post['data']['title']}\n\n"
                f"*Text:* {most_popular_post['data']['selftext']}\n\n"
                f"[Link](https://www.reddit.com{most_popular_post['data']['permalink']})"
            )
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown')
            logger.info("Sent the most popular post to the user.")

        except Exception as e:
            logger.error(f"Error while fetching/sending posts: {e}")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: {e}")
    def run(self):
        """
        Starts the bot and begins polling for messages.
        """
        logger.info("Telegram bot started.")
        self.application.run_polling()

if __name__ == '__main__':
    # Initialize RedditClient with environment variables
    reddit_client = RedditClient(client_id, client_secret, username, password, user_agent)
    # Create and run the Telegram bot
    bot = TelegramBot(bot_token, reddit_client)
    bot.run()
