def check_trending_coins(api_client):
    """
    Check for trending MemeCoins based on social media activity.
    Returns a list of trending coins with their price and social metrics.
    """
    try:
        trending_coins = api_client.get_trending_coins()
        if not trending_coins:
            return []
        
        # Filter and sort by social activity
        trending_coins = [
            coin for coin in trending_coins 
            if coin.get('social_score', 0) > 0
        ]
        trending_coins.sort(key=lambda x: x.get('social_score', 0), reverse=True)
        
        return trending_coins[:10]  # Return top 10 trending coins
    except Exception as e:
        print(f"Error fetching trending coins: {e}")
        return []

def notify_users(trending_coins, notification_service):
    """
    Notify users about the trending MemeCoins.
    """
    for coin in trending_coins:
        message = f"🚀 Trending MemeCoin: {coin['name']} - Price: {coin['price']}"
        notification_service.send_notification(message)

def main(api_client, notification_service):
    """
    Main function to check for trending MemeCoins and notify users.
    """
    trending_coins = check_trending_coins(api_client)
    if trending_coins:
        notify_users(trending_coins, notification_service)