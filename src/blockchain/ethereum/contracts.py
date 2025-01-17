from web3 import Web3
from typing import Dict, Any

class EthereumContract:
    def __init__(self, address: str, abi: Dict[str, Any], web3_instance: Web3):
        """
        Initialize an Ethereum contract interface.
        
        Args:
            address: The contract's address on the blockchain
            abi: The contract's ABI (Application Binary Interface)
            web3_instance: An initialized Web3 instance
        """
        self.address = Web3.to_checksum_address(address)
        self.abi = abi
        self.web3 = web3_instance
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)

    def call_function(self, function_name: str, *args, **kwargs) -> Any:
        """
        Call a read-only contract function.
        
        Args:
            function_name: Name of the contract function to call
            *args: Function arguments
            **kwargs: Additional parameters for the function call
        """
        contract_function = getattr(self.contract.functions, function_name)
        return contract_function(*args).call(**kwargs)

    def send_transaction(self, function_name: str, account: str, *args, **kwargs) -> str:
        """
        Send a transaction to a contract function.
        
        Args:
            function_name: Name of the contract function to call
            account: The sender's account address
            *args: Function arguments
            **kwargs: Additional transaction parameters
        
        Returns:
            Transaction hash
        """
        contract_function = getattr(self.contract.functions, function_name)
        transaction = contract_function(*args).build_transaction({
            'from': Web3.to_checksum_address(account),
            'nonce': self.web3.eth.get_transaction_count(account),
            **kwargs
        })
        return transaction