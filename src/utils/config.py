import os
import logging
from dotenv import load_dotenv
from dataclasses import dataclass

@dataclass
class Config:
    telegram_token: str
    web3_provider: str
    wallet_address: str
    private_key: str
    min_profit_margin: float
    trade_amount: float
    gas_limit: int
    max_slippage: float

logger = logging.getLogger(__name__)

def load_config() -> Config:
    if not load_dotenv():
        logger.error("Could not find .env file")
        raise EnvironmentError("Could not find .env file")
    
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    if not telegram_token:
        logger.error("TELEGRAM_TOKEN is missing in .env file")
        raise ValueError("TELEGRAM_TOKEN is required in .env file")
    
    logger.info(f"Loaded configuration with token length: {len(telegram_token)}")
    
    web3_provider = os.getenv('WEB3_PROVIDER_URL')
    if not web3_provider:
        raise ValueError("WEB3_PROVIDER_URL is required in .env file")
    
    return Config(
        telegram_token=telegram_token,
        web3_provider=web3_provider,
        wallet_address=os.getenv('WALLET_ADDRESS', ''),
        private_key=os.getenv('PRIVATE_KEY', ''),
        min_profit_margin=float(os.getenv('MIN_PROFIT_MARGIN', '1.0')),
        trade_amount=float(os.getenv('TRADE_AMOUNT', '0.1')),
        gas_limit=int(os.getenv('GAS_LIMIT', '300000')),
        max_slippage=float(os.getenv('MAX_SLIPPAGE', '0.5'))
    )

__all__ = ['Config', 'load_config']