import requests
from src.logger import logger

def send_telegram_message(bot_token, chat_id, message):
    """
    Sends a message to a Telegram chat using a bot.

    Parameters:
    bot_token (str): The API token for the bot from BotFather.
    chat_id (str or int): The chat ID where the message will be sent.
    message (str): The message content to send.
    """
    # Define the URL for the Telegram API
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # Define the payload for the message
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    
    # Send the request
    response = requests.post(url, data=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        logger("Alert sent to Telegram.")
    else:
        logger.error(f"Failed to send message. Error code: {response.status_code}")
