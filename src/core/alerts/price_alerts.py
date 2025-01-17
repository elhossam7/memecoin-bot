def check_price_alerts(current_price, target_price):
    """
    Check if the current price has reached the target price for alerting.
    
    Parameters:
    - current_price (float): The current price of the MemeCoin.
    - target_price (float): The target price to trigger the alert.
    
    Returns:
    - bool: True if the current price meets or exceeds the target price, False otherwise.
    """
    return current_price >= target_price


def notify_user(user_id, message):
    """
    Notify the user via Telegram when a price alert is triggered.
    
    Parameters:
    - user_id (str): The Telegram user ID to send the notification to.
    - message (str): The message to be sent to the user.
    """
    # Implementation for sending a message to the user via Telegram API
    try:
        # You would need to initialize your bot with a token first
        bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
        bot.send_message(chat_id=user_id, text=message)
    except telegram.error.TelegramError as e:
        logging.error(f"Failed to send Telegram message: {e}")


def set_price_alert(user_id, target_price):
    """
    Set a price alert for the user.
    
    Parameters:
    - user_id (str): The Telegram user ID setting the alert.
    - target_price (float): The target price for the alert.
    """
    # Store the user's alert settings in a database or in-memory structure
    # Create an in-memory dictionary to store alerts if not exists
    if not hasattr(set_price_alert, 'alerts'):
        set_price_alert.alerts = {}

    # Store the alert
    set_price_alert.alerts[user_id] = target_price
    logging.info(f"Price alert set for user {user_id} at {target_price}")
    pass


def check_and_notify(current_price, user_alerts):
    """
    Check all user alerts and notify if any price thresholds are met.
    
    Parameters:
    - current_price (float): The current price of the MemeCoin.
    - user_alerts (dict): A dictionary of user IDs and their target prices.
    """
    for user_id, target_price in user_alerts.items():
        if check_price_alerts(current_price, target_price):
            notify_user(user_id, f"Price alert! The current price is {current_price}, which meets your target of {target_price}.")