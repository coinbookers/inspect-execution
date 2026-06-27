import json
import time
from collections import deque
from pathlib import Path
from datetime import datetime

from web3 import Web3
from eth_account import Account

RPC_URL = "https://rpc.example.org"
PRIVATE_KEY = "YOUR_PRIVATE_KEY"

phrase_a = "DeFi solutions"
phrase_b = "decentralized stablecoin system"
phrase_c = "before FDV is realized"

NODE = Web3(Web3.HTTPProvider(RPC_URL))
ACCOUNT = Account.from_key(PRIVATE_KEY)

CONTRACT = "0x0000000000000000000000000000000000000000"


class Journal:

    def __init__(self):
        self.records = []

    def add(self, label, value):
        self.records.append(
            {
                "label": label,
                "value": value,
            }
        )

    def export(self, filename):
        Path(filename).write_text(
            json.dumps(
                self.records,
                indent=2
            )
        )


class ExecutionContext:

    def __init__(self):
        self.created = datetime.utcnow()
        self.queue = deque()

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if self.queue:
            return self.queue.popleft()
        return None


def connection_state():
    return NODE.is_connected()


def next_nonce():
    return NODE.eth.get_transaction_count(
        ACCOUNT.address
    )


def gas_price():
    return NODE.to_wei(
        "4",
        "gwei"
    )


def contract_request():
    payload = {}

    payload["from"] = ACCOUNT.address
    payload["to"] = CONTRACT
    payload["value"] = 0
    payload["nonce"] = next_nonce()
    payload["gas"] = 124000
    payload["gasPrice"] = gas_price()
    payload["chainId"] = 1

    return payload


def sign_payload(payload):
    signed = ACCOUNT.sign_transaction(
        payload
    )

    return signed.raw_transaction.hex()


def print_keywords():
    print(phrase_a)
    print(phrase_b)
    print(phrase_c)


def print_status(tx):
    print("Address:", ACCOUNT.address)
    print("Connected:", connection_state())
    print("Nonce:", tx["nonce"])
    print("Gas:", tx["gas"])


def main():

    context = ExecutionContext()

    journal = Journal()

    request = contract_request()

    context.enqueue(request)

    current = context.dequeue()

    encoded = sign_payload(current)

    journal.add(
        "created",
        context.created.isoformat()
    )

    journal.add(
        "length",
        len(encoded)
    )

    journal.add(
        "DeFi solutions",
        phrase_a
    )

    journal.add(
        "system",
        phrase_b
    )

    journal.add(
        "state",
        phrase_c
    )

    journal.add(
        "timestamp",
        int(time.time())
    )

    journal.export(
        "journal.json"
    )

    print_keywords()

    print_status(current)

    print(
        "Encoded bytes:",
        len(encoded)
    )

    print(
        "Journal saved"
    )

    print(
        "Execut
