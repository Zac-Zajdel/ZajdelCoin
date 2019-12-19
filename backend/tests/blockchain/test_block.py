import time

from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary


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


def test_genesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)

    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value
