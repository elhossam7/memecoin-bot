import { ethWallet as wallet, solanaWallet } from './wallet';

async function displayWalletInfo() {
    // ...existing code...
    console.log('\n💼 Your Wallets:');
    console.log(`ETH Address: ${wallet.getAddress()}`);
    console.log(`ETH Balance: ${await wallet.getBalance()} ETH`);
    console.log(`SOL Address: ${solanaWallet.getAddress()}`);
    console.log(`SOL Balance: ${await solanaWallet.getBalance()} SOL`);
    // ...existing code...
}

// ...rest of the existing code...
