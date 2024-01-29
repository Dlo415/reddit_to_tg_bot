# Reddit Telegram Bot

## Description
The Reddit Telegram Bot is an automated bot for Telegram that provides users the ability to fetch and view the latest posts from selected subreddits on Reddit. The bot's primary functionality includes retrieving the most popular posts from Reddit and displaying them within a Telegram chat.

## How the Bot Works
The Reddit Telegram Bot operates using a simple yet effective algorithm to bring you the most popular posts from your chosen subreddit. Here's a step-by-step breakdown of how the bot functions:

1. **Fetching Posts**: When a command for a specific subreddit is received (e.g., `/python`), the bot interacts with the Reddit API to fetch the latest 20 posts from the 'new' section of the specified subreddit.

2. **Identifying Popular Posts**: Among these 20 posts, the bot identifies the most popular post — the one with the highest number of upvotes (also known as 'score' in Reddit terminology).

3. **Delivering Content**: The bot then formats a message that includes the title, a brief description (if available), and a direct link to this most popular post. This message is sent back to you through the Telegram chat.

By using this approach, the bot ensures that you're always presented with the freshest and most engaging content from the Reddit community without having to manually sift through the subreddit yourself.

## Technologies
- Python 3.8+
- python-telegram-bot
- requests

## Installation
To use this bot, you need to have Python 3.8 or higher installed along with the following libraries:
 - pip install python-telegram-bot requests python-dotenv

## Configuration
Before running the bot, you need to create a `.env` file in the project's root directory and fill it with the following environment variables:
- CLIENT_ID=your_reddit_client_id
- CLIENT_SECRET=your_reddit_client_secret
- USERNAME=your_reddit_username
- PASSWORD=your_reddit_password 
- USER_AGENT='your_user_agent_for_reddit'
- BOT_TOKEN=your_telegram_bot_token

## Running
Before interacting with the bot, you need to start it. To run the bot, navigate to the project directory in your terminal and execute the following command:
- python -m app.telegram.telegram_bot

## Bot Commands
To interact with the bot, you will need to send commands through the Telegram UI. Make sure you have started the bot using the instructions provided in the [Running](#running) section. Once the bot is running, you can use the following commands in the Telegram chat:
- `/start` - start interacting with the bot.
- `/learnpython` - get popular posts from the learnpython subreddit.
- `/python` - get popular posts from the python subreddit.
- `/learnprogramming` - get popular posts from the learnprogramming subreddit.
- `/chatgpt` - get popular posts from the chatgpt subreddit.
- `/qualityassurance` - get popular posts from the qualityassurance subreddit.
- `/cscareerquestions` - get popular posts from the cscareerquestions subreddit.
- `/softwaretesting` - get popular posts from the softwaretesting subreddit.




