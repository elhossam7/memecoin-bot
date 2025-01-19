import logging
from eth_account import Account
import secrets
import base58
from typing import Dict, Any, Tuple
import os
import binascii

logger = logging.getLogger(__name__)

# Fix Solana imports
try:
    from solana.keypair import Keypair
    SOLANA_AVAILABLE = True
except ImportError:
    logger.warning("Solana SDK not available. Using fallback wallet generation.")
    SOLANA_AVAILABLE = False

class WalletGenerator:
    @staticmethod
    def generate_ethereum_wallet() -> Tuple[str, str]:
        """Generate a new Ethereum wallet address and private key."""
        Account.enable_unaudited_hdwallet_features()
        acct = Account.create(secrets.token_hex(32))
        return acct.address, acct.key.hex()

    @staticmethod
    def generate_solana_wallet() -> Tuple[str, str]:
        """Generate a new Solana wallet address and private key."""
        try:
            if not SOLANA_AVAILABLE:
                raise ImportError("Solana SDK not available")
                
            keypair = Keypair.generate()
            public_key = str(keypair.public_key)
            private_key = base58.b58encode(bytes(keypair.secret_key)).decode('ascii')
            return public_key, private_key
            
        except ImportError:
            # Fallback to basic key generation
            private_key = binascii.hexlify(os.urandom(32)).decode('ascii')
            public_key = f"Solana{private_key[:32]}"
            logger.warning("Using fallback Solana wallet generation")
            return public_key, private_key

    @staticmethod
    def create_wallet(chain: str) -> Dict[str, Any]:
        """Create a new wallet for specified chain"""
        try:
            if chain.lower() == 'solana':
                public_key, private_key = WalletGenerator.generate_solana_wallet()
                return {
                    'solana': {
                        'address': public_key,
                        'private_key': private_key,
                        'success': True
                    }
                }
            else:
                raise ValueError(f"Unsupported chain: {chain}")
                
        except Exception as e:
            logger.error(f"Error creating wallet: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    @classmethod
    def create_wallets(cls, primary_blockchain: str) -> Dict[str, Any]:
        """Create wallets for both blockchains, setting the chosen one as primary."""
        # Generate both wallets
        eth_address, eth_private_key = cls.generate_ethereum_wallet()
        sol_address, sol_private_key = cls.generate_solana_wallet()

        return {
            'primary_blockchain': primary_blockchain.lower(),
            'ethereum': {
                'address': eth_address,
                'private_key': eth_private_key,
            },
            'solana': {
                'address': sol_address,
                'private_key': sol_private_key,
            }
        }
