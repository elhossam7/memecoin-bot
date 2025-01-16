def connect_to_solana():
    """
    Connects to the Solana blockchain using the Solana Web3 library.
    Returns the connection object.
    """
    from solana.rpc.api import Client

    # Replace with your Solana cluster URL
    solana_cluster_url = "https://api.mainnet-beta.solana.com"
    client = Client(solana_cluster_url)
    return client


def get_account_balance(public_key):
    """
    Retrieves the balance of a given Solana account.
    
    Args:
        public_key (str): The public key of the Solana account.
    
    Returns:
        float: The balance of the account in SOL.
    """
    client = connect_to_solana()
    balance = client.get_balance(public_key)
    return balance['result']['value'] / 1_000_000_000  # Convert lamports to SOL


def send_transaction(transaction):
    """
    Sends a transaction to the Solana blockchain.
    
    Args:
        transaction (Transaction): The transaction object to send.
    
    Returns:
        str: The transaction signature.
    """
    client = connect_to_solana()
    response = client.send_transaction(transaction)
    return response['result']