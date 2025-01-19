from cryptography.fernet import Fernet
import json
import os
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class WalletStorage:
    def __init__(self):
        self.key = os.getenv('ENCRYPTION_KEY') or Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.storage_path = 'data/wallets/'
        os.makedirs(self.storage_path, exist_ok=True)

    def save_wallet(self, user_id: str, wallet_data: Dict) -> bool:
        """Encrypt and save wallet data for a user."""
        try:
            # Encrypt sensitive data
            encrypted_data = self.cipher_suite.encrypt(
                json.dumps(wallet_data).encode()
            )
            
            # Save to file
            with open(f"{self.storage_path}{user_id}.wallet", 'wb') as f:
                f.write(encrypted_data)
            return True
        except Exception as e:
            print(f"Error saving wallet: {e}")
            return False

    def get_wallet(self, user_id: str) -> Optional[Dict]:
        """Retrieve and decrypt wallet data for a user."""
        try:
            with open(f"{self.storage_path}{user_id}.wallet", 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Error retrieving wallet: {e}")
            return None
