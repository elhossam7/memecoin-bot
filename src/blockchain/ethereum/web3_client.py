from web3 import Web3

class EthereumClient:
    def __init__(self, infura_url):
        self.web3 = Web3(Web3.HTTPProvider(infura_url))
        if not self.web3.isConnected():
            raise Exception("Failed to connect to Ethereum network")

    def get_balance(self, address):
        balance_wei = self.web3.eth.get_balance(address)
        return self.web3.fromWei(balance_wei, 'ether')

    def send_transaction(self, from_address, to_address, value, private_key):
        nonce = self.web3.eth.getTransactionCount(from_address)
        transaction = {
            'to': to_address,
            'value': self.web3.toWei(value, 'ether'),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': nonce,
        }
        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key)
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return txn_hash.hex()

    def get_transaction_receipt(self, txn_hash):
        return self.web3.eth.getTransactionReceipt(txn_hash)