import os
import json
from datetime import datetime
from eth_account import Account
from web3 import Web3
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class WalletManager:
    def __init__(self, storage_path: str = "data/wallets"):
        """Initialize WalletManager with storage path"""
        try:
            self.storage_path = Path(storage_path)
            self.storage_path.mkdir(parents=True, exist_ok=True)
            
            # Get provider URL from environment
            provider_url = os.getenv('WEB3_PROVIDER_URL')
            if not provider_url:
                logger.warning("WEB3_PROVIDER_URL not found, using default Infura endpoint")
                provider_url = "https://mainnet.infura.io/v3/f13e47cbf64f4ccdb9d5474c06cdf7a0"
            
            # Initialize Web3 with multiple provider attempts
            self.web3 = self._initialize_web3(provider_url)
            
        except Exception as e:
            logger.error(f"Error initializing WalletManager: {str(e)}")
            raise

    def _initialize_web3(self, provider_url: str) -> Web3:
        """Initialize Web3 with fallback providers"""
        providers = [
            provider_url,
            "https://eth-mainnet.public.blastapi.io",
            "https://rpc.ankr.com/eth",
            "https://cloudflare-eth.com"
        ]
        
        for provider in providers:
            try:
                web3 = Web3(Web3.HTTPProvider(provider))
                if web3.is_connected():
                    logger.info(f"Successfully connected to Web3 provider: {provider}")
                    return web3
            except Exception as e:
                logger.warning(f"Failed to connect to provider {provider}: {str(e)}")
                continue
        
        # If we get here, no providers worked
        raise ConnectionError("Failed to connect to any Web3 provider")

    def create_wallet(self, user_id: int) -> Dict[str, Any]:
        """Create a new wallet for a user"""
        try:
            Account.enable_unaudited_hdwallet_features()
            acct = Account.create()
            
            wallet_data = {
                'address': acct.address,
                'private_key': acct.key.hex(),
                'created_at': datetime.utcnow().isoformat(),
                'balance': 0.0,
                'user_id': user_id
            }

            self._save_wallet_data(user_id, wallet_data)
            
            return {
                'address': wallet_data['address'],
                'success': True,
                'message': 'Wallet created successfully'
            }
            
        except Exception as e:
            error_msg = f"Error creating wallet: {str(e)}"
            logger.error(f"User {user_id}: {error_msg}")
            return {
                'success': False,
                'message': error_msg
            }

    def get_wallet(self, user_id: int) -> dict:
        """Get user's wallet information"""
        try:
            wallet_data = self._load_wallet_data(user_id)
            if wallet_data:
                # Update balance
                balance = self.web3.eth.get_balance(wallet_data['address'])
                wallet_data['balance'] = self.web3.from_wei(balance, 'ether')
                return wallet_data
            return None
        except Exception as e:
            logger.error(f"Error getting wallet for user {user_id}: {e}")
            return None

    def _save_wallet_data(self, user_id: int, wallet_data: dict):
        """Save wallet data to secure storage"""
        try:
            file_path = self.storage_path / f"{user_id}.json"
            with open(file_path, 'w') as f:
                json.dump(wallet_data, f)
        except Exception as e:
            logger.error(f"Error saving wallet data: {e}")
            raise

    def _load_wallet_data(self, user_id: int) -> dict:
        """Load wallet data from storage"""
        try:
            file_path = self.storage_path / f"{user_id}.json"
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Error loading wallet data: {e}")
            return None
