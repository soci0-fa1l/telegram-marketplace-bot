from __future__ import annotations
import os
from typing import Optional, Dict
from web3 import Web3
from eth_account import Account


def _get_web3(rpc_url: Optional[str] = None) -> Web3:
    url = rpc_url or os.environ.get("RPC_URL")
    if not url:
        raise ValueError("RPC_URL environment variable not set")
    return Web3(Web3.HTTPProvider(url))


def create_wallet() -> Dict[str, str]:
    """Create a new wallet and return address and private key."""
    acct = Account.create()
    return {"address": acct.address, "private_key": acct.key.hex()}


def get_balance(address: str, rpc_url: Optional[str] = None) -> float:
    w3 = _get_web3(rpc_url)
    balance_wei = w3.eth.get_balance(Web3.to_checksum_address(address))
    return w3.from_wei(balance_wei, "ether")


def send_payment(private_key: str, to_address: str, amount_eth: float, rpc_url: Optional[str] = None) -> str:
    w3 = _get_web3(rpc_url)
    account = w3.eth.account.from_key(private_key)
    tx = {
        "to": Web3.to_checksum_address(to_address),
        "value": w3.to_wei(amount_eth, "ether"),
        "gas": 21000,
        "gasPrice": w3.to_wei("50", "gwei"),
        "nonce": w3.eth.get_transaction_count(account.address),
    }
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()
