import pytest
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA


def test_blockchain_instance():
    blockchain = Blockchain()
    assert blockchain.chain[0].hash == GENESIS_DATA['hash']


def test_add_block():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)
    assert blockchain.chain[-1].data == data

@pytest.fixture
def blockchain_three_blocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block(i)
    return blockchain

# Passes if no exception is raised.
def test_is_valid_chain(blockchain_three_blocks):
    Blockchain.is_valid_chain(blockchain_three_blocks.chain)

def test_is_valid_chain_bad_genesis(blockchain_three_blocks):
    blockchain_three_blocks.chain[0].hash = 'bas_hash'
    with pytest.raises(Exception, match='The genesis block must be valid.'):
      Blockchain.is_valid_chain(blockchain_three_blocks.chain)

# Tests that the local blockchain instance now equals the fixture
def test_replace_chain(blockchain_three_blocks):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_three_blocks.chain)

    assert blockchain.chain == blockchain_three_blocks.chain

# len(blockchain_three_blocks) > len(blockchain). This tests makes that forced condition fail.
def test_replace_chain_invalid_length(blockchain_three_blocks):
    blockchain = Blockchain()
    
    with pytest.raises(Exception, match='Cannot replace. The incoming chain must be longer.'):
      blockchain_three_blocks.replace_chain(blockchain.chain)

def test_replace_chain_bad_chain(blockchain_three_blocks):
    blockchain = Blockchain()
    blockchain_three_blocks.chain[1].hash = 'bad_hash'

    with pytest.raises(Exception, match='The incoming chain is invalid.'):
      blockchain.replace_chain(blockchain_three_blocks.chain)

