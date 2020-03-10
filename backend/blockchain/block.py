import time
from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE

# Initial data used to start the blockchain
GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}


class Block:
    """
    Block: unit of storage
    Store transaction in a blockchain that supports Zajdelcoin
    """

    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )

    # Used to allow comparison on the items existing in two seperate instances.
    def __eq__(self, other):
      return self.__dict__ == other.__dict__

    def to_json(self):
        """
        Serialize the block into a dictionary of its attributes.
        """
        return self.__dict__



    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data until Proof-Of-Work requirement is fulfilled
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

      # Perpetually loops until the leading zero's of hash equals the difficulty value.
        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculates the difficulty of mining blocking according to the MINE_RATE.
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        # Makes certain that the difficulty can never go less than zero.
        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validate a block by enforcing the following rules:
          1. The block must have the proper last_hash reference.
          2. The block must meet the proof-of-work requirement.
          3. The difficulty must only adjust by one.
          4. The block hash must be a valid combination of the block fields.
            - This will ensure authenticity that the block's data has not been tampered with. 
            - last_hash MUST EQUAL current_block's for it to be valid and added to the chain.
        """

        if block.last_hash != last_block.hash:
            raise Exception(
                'The block last_hash does not equal the last_blocks hash value.')

        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('The proof-of-work requirement was not met.')

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('Difficulty adjusted by more than one degree.')

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.nonce,
            block.difficulty
        )

        if block.hash != reconstructed_hash:
            raise Exception(
                'The block hash must be correct. Data was corrupted/tampered')

    @staticmethod
    def genesis():
        """
        Generate the genesis block.
        """
        return Block(**GENESIS_DATA)

    @staticmethod
    def from_json(block_json):
        """
        Deserialize block's json representation back into a block instance.
        """
        return Block(**block_json)


def main():
    genesis_block = Block.genesis()

    # Purposely messing up last hash to cause issue.
    bad_block = Block.mine_block(genesis_block, 'test_data')
    bad_block.last_hash = 'wrong_data'

    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:
        print(f'is valid_block: {e}')


if __name__ == '__main__':
    main()
