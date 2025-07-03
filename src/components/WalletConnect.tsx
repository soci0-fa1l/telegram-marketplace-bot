import React, { useState } from 'react';
import { Wallet } from 'lucide-react';

declare global {
  interface Window {
    ethereum?: any;
    trustwallet?: any;
    tp?: any;
  }
}

const WalletConnect: React.FC = () => {
  const [account, setAccount] = useState<string | null>(null);

  const connect = async () => {
    const provider = window.ethereum || (window as any).trustwallet || (window as any).tp;
    if (!provider) {
      alert('지원되는 지갑이 설치되어 있지 않습니다.');
      return;
    }
    try {
      const accounts = await provider.request({ method: 'eth_requestAccounts' });
      setAccount(accounts[0]);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      {account ? (
        <span className="text-xs text-gray-600">{account.slice(0, 6)}...{account.slice(-4)}</span>
      ) : (
        <button
          onClick={connect}
          className="p-2 rounded-lg bg-blue-500 text-white hover:bg-blue-600"
          aria-label="지갑 연결"
        >
          <Wallet className="w-4 h-4" />
        </button>
      )}
    </div>
  );
};

export default WalletConnect;