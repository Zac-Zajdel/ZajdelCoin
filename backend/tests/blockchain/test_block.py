import time
import pytest

from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary


def test_genesis():
    genesis = Block.genesis()
    assert isinstance(genesis, Block)

    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value


def test_mine_block():
    last_block = Block.genesis()
    data = 'testing-data'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[
        0:block.difficulty] == '0' * block.difficulty


def test_quickly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'test')
    mined_block = Block.mine_block(last_block, 'test2')

    # Should be one higher since its timestamp is less than rate
    assert mined_block.difficulty == last_block.difficulty + 1


def test_slowly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'test')

    time.sleep(MINE_RATE / SECONDS)

    mined_block = Block.mine_block(last_block, 'test2')

    # Should be one lower due to its delay
    assert mined_block.difficulty == last_block.difficulty - 1


def test_mined_block_difficulty_limits_at_1():
    last_block = Block(
        time.time_ns(),
        'test_last',
        'test_hash',
        'test_data',
        1,
        0
    )

    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'test2')

    assert mined_block.difficulty == 1


@pytest.fixture
def last_block():
    return Block.genesis()


@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, 'test_data')


def test_is_valid_block(last_block, block):
    Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_last_hash(last_block, block):
    block.last_hash = 'manipulated_hash'

    with pytest.raises(Exception, match='The block last_hash does not equal the last_blocks hash value.'):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_proof_of_work(last_block, block):
    block.hash = 'fff'

    with pytest.raises(Exception, match='The proof-of-work requirement was not met.'):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_jumped_difficulty(last_block, block):
    jumped_difficulty = 10
    block.difficulty = jumped_difficulty
    block.hash = f'{"0" * jumped_difficulty}'

    with pytest.raises(Exception, match='Difficulty adjusted by more than one degree.'):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_hash(last_block, block):
    # Leading this hash with all zero's allows us to pass the proof-of-work concepts
    # Truly tests the last line of defense against our corrupted data by ensuring our check on the hash on our side.
    block.hash = '000000000000000000000bbbabc'

    with pytest.raises(Exception, match='The block hash must be correct. Data was corrupted/tampered'):
        Block.is_valid_block(last_block, block)
