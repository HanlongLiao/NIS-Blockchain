import flake8
import requests
import hashlib
import json

from time import time
from uuid import uuid4


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transaction = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        '''
         Create a new block, and adds it to chain
        :param proof: <int> The proof given by the proof of work algorithm
        :param previous_hash: (Optional) <str> Hash of previous block
        :return: <dict> New block
        '''

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transaction,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # Request the current list of transaction
        self.current_transaction = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        '''
        Create a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the recipient
        :param amount: <int> Amount
        :return: <int> The index of the block that will hold this transaction
        '''

        self.current_transaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        '''
        Create a SHA-256 hash of a block
        :param block: <dict> Block
        :return: <str>
        '''

        # we must make sure that the dictionary is ordered, or we'll have inconsistent hashes
        block_string = json.dump(block, sort_keys=True).encode()
        return hashlib.sha_256(block_string).hexdigest()

    @property
    def last_block(self):
       return self.chain[-1]


if __name__ == '__main__':
    pass