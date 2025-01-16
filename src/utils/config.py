import os

class Config:
    # Telegram Bot Token
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your-telegram-bot-token")

    # Ethereum Configuration
    ETHEREUM_RPC_URL = os.getenv("ETHEREUM_RPC_URL", "https://mainnet.infura.io/v3/your-infura-project-id")
    ETHEREUM_PRIVATE_KEY = os.getenv("ETHEREUM_PRIVATE_KEY", "your-ethereum-private-key")

    # Solana Configuration
    SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    SOLANA_PRIVATE_KEY = os.getenv("SOLANA_PRIVATE_KEY", "your-solana-private-key")

    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/memecoin_bot")

    # Other Constants
    MAX_SLIPPAGE = 0.5  # Maximum slippage percentage
    TRADE_TIMEOUT = 30  # Timeout for trade execution in seconds