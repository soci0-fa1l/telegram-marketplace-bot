import React, { useState } from 'react';

declare global {
  interface Window {
    ethereum?: any;
  }
}

const WalletConnect: React.FC = () => {
  const [account, setAccount] = useState<string | null>(null);

  const connectWallet = async () => {
    if (!window.ethereum) {
      alert('MetaMask가 설치되어 있지 않습니다.');
      return;
    }
    try {
      const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
      setAccount(accounts[0]);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      {account ? (
        <p>지갑 주소: {account}</p>
      ) : (
        <button onClick={connectWallet}>지갑 연결</button>
      )}
    </div>
  );
};

export default WalletConnect;
