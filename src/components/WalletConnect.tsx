import React, { useState } from 'react';

declare global {
  interface Window {
    ethereum?: any;
    trustwallet?: any;
    tp?: any;
  }
}

const WalletConnect: React.FC = () => {
  const [account, setAccount] = useState<string | null>(null);

  const requestAccounts = async (provider: any) => {
    const accounts = await provider.request({ method: 'eth_requestAccounts' });
    setAccount(accounts[0]);
  };

  const connectMetaMask = async () => {
    const provider = window.ethereum;
    if (!provider) {
      alert('MetaMask가 설치되어 있지 않습니다.');
      return;
    }
    try {
      await requestAccounts(provider);
    } catch (err) {
      console.error(err);
    }
  };

  const connectTrustWallet = async () => {
    const provider = window.ethereum?.isTrust ? window.ethereum : (window as any).trustwallet;
    if (!provider) {
      alert('Trust Wallet이 설치되어 있지 않습니다.');
      return;
    }
    try {
      await requestAccounts(provider);
    } catch (err) {
      console.error(err);
    }
  };

  const connectTokenPocket = async () => {
    const provider = window.ethereum?.isTokenPocket ? window.ethereum : (window as any).tp;
    if (!provider) {
      alert('TokenPocket이 설치되어 있지 않습니다.');
      return;
    }
    try {
      await requestAccounts(provider);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      {account ? (
        <p>지갑 주소: {account}</p>
      ) : (
        <div>
          <button onClick={connectMetaMask}>MetaMask 연결</button>
          <button onClick={connectTrustWallet}>Trust Wallet 연결</button>
          <button onClick={connectTokenPocket}>TokenPocket 연결</button>
        </div>
      )}
    </div>
  );
};

export default WalletConnect;
