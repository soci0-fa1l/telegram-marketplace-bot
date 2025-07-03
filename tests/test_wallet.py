import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api import crypto_wallet


def test_create_wallet():
    wallet = crypto_wallet.create_wallet()
    assert "address" in wallet and "private_key" in wallet
    assert wallet["address"].startswith("0x")
    # private keys returned by eth_account do not include a 0x prefix
    assert len(wallet["private_key"]) >= 64
