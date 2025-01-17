from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.transaction import AccountMeta
from solana.publickey import PublicKey
from solana.system_program import SYS_PROGRAM_ID
from spl.token.instructions import get_associated_token_address

class SolanaContracts:
    def __init__(self, rpc_url: str):
        self.client = Client(rpc_url)
        
    async def get_token_balance(self, token_address: str, wallet_address: str) -> float:
        """Get token balance for a specific wallet"""
        try:
            # Convert addresses to PublicKey objects
            token_pubkey = PublicKey(token_address)
            wallet_pubkey = PublicKey(wallet_address)
            
            # Get the associated token account address
            ata = get_associated_token_address(wallet_pubkey, token_pubkey)
            
            # Get the balance
            response = await self.client.get_token_account_balance(str(ata))
            return float(response['result']['value']['amount'])
        except Exception as e:
            print(f"Error getting token balance: {e}")
            return 0.0