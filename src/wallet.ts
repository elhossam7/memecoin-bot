import { Connection, PublicKey, Keypair } from '@solana/web3.js';
import Web3 from 'web3';
import { Account } from 'web3-core';

export class EthereumWallet {
    private web3: Web3;
    private account: Account;

    constructor() {
        this.web3 = new Web3('https://mainnet.infura.io/v3/YOUR_INFURA_KEY');
        this.account = this.web3.eth.accounts.create();
    }

    async getBalance(): Promise<string> {
        const balance = await this.web3.eth.getBalance(this.account.address);
        return this.web3.utils.fromWei(balance, 'ether');
    }

    getAddress(): string {
        return this.account.address;
    }
}

export class SolanaWallet {
    private connection: Connection;
    private keypair: Keypair;

    constructor() {
        this.connection = new Connection('https://api.mainnet-beta.solana.com');
        this.keypair = Keypair.generate();
    }

    async getBalance(): Promise<number> {
        const balance = await this.connection.getBalance(this.keypair.publicKey);
        return balance / 1e9; // Convert lamports to SOL
    }

    getAddress(): string {
        return this.keypair.publicKey.toString();
    }
}

export const solanaWallet = new SolanaWallet();
export const ethWallet = new EthereumWallet();
