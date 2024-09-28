import requests

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
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Error code: {response.status_code}")
        print("Response:", response.json())

# Example usage:
if __name__ == "__main__":
    # Replace these with your bot's token and chat ID
    bot_token = "YOUR_BOT_TOKEN_HERE"
    chat_id = "YOUR_CHAT_ID_HERE"
    message = "Hello! This is a test message from my Python script."

    # Call the function to send the message
    send_telegram_message(bot_token, chat_id, message)
