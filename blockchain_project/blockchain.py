import json
import time
from hashlib import sha256

class Block:
    """Class representing a single block in the blockchain."""

    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        """
        Initializes a new block object.

        :param index: Index of the block in the blockchain.
        :param transactions: List of transactions included in the block.
        :param timestamp: Time at which the block was created.
        :param previous_hash: Hash of the previous block in the blockchain.
        :param nonce: Counter used during proof of work.
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        """
        Computes the hash of the block based on its attributes.

        :return: The generated hash of the block.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

class Blockchain:
    """Class representing the blockchain."""

    difficulty = 2

    def __init__(self):
        """Initializes a new blockchain."""
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Creates the genesis block (first block) in the blockchain."""
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        """Returns the last block in the blockchain."""
        return self.chain[-1]

    def proof_of_work(self, block):
        """
        Executes proof of work on a given block.

        :param block: The block on which proof of work is to be executed.
        :return: The generated hash of the block after proof of work.
        """
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        """
        Adds a block to the blockchain after validation.

        :param block: The block to be added to the blockchain.
        :param proof: The proof of work for the block.
        :return: True if the block is added successfully, False otherwise.
        """
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Checks if the provided block hash satisfies the proof of work criteria.

        :param block: The block to be validated.
        :param block_hash: The hash of the block to be validated.
        :return: True if the block hash satisfies the proof of work criteria, False otherwise.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
        """
        Adds a new transaction to the list of unconfirmed transactions.

        :param transaction: The transaction to be added.
        """
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        Mines a new block by including pending transactions.

        :return: The index of the newly mined block.
        """
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index
