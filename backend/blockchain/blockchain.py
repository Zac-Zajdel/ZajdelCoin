from backend.blockchain.block import Block

class Blockchain:
  """
  Blockchain: a public ledger of transactions.
  Implemented as a list of blocks - data sets of transactions
  """

  def __init__(self):
    self.chain = [Block.genesis()]

  def __repr__(self):
    return f'Blockchain: {self.chain}'

  def add_block(self, data):
    self.chain.append(Block.mine_block(self.chain[-1], data))

  def to_json(self):
    """
    Serialize the blockchain into a list of blocks by mapping over each block
    inside the chain and calling the blocks to_json() method which returns
    its dictionary value.
    """
    return list(map(lambda block: block.to_json(), self.chain))

  @staticmethod
  def from_json(chain_json):
    """
    Deserialize a list of serialized blocks into a Blockchain instance.
    The result will contain a chain list of Block instances.
    """
    blockchain = Blockchain()
    blockchain.chain = list(map(lambda block_json: Block.from_json(block_json), chain_json))

    return blockchain

  def replace_chain(self, chain):
    """
    Replace the local chain with the incoming one if the following applies:
      1. The incoming chain must be longer then the local one.
      2. Incoming chain is formatted properly.
    """
    if len(chain) <= len(self.chain):
      raise Exception('Cannot replace. The incoming chain must be longer.')

    try:
      Blockchain.is_valid_chain(chain)
    except Exception as e:
      raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')

    self.chain = chain

  @staticmethod
  def is_valid_chain(chain):
    """
    Validates the incoming blockchain.
    Enforce the following rules of the blockchain:
      - The chain must start with the genesis block.
      - Blocks must be formatted correctly.
    """
    if chain[0] != Block.genesis():
      raise Exception('The genesis block must be valid.')

    for i in range(1, len(chain)):
      block = chain[i]
      last_block = chain[i - 1]
      block.is_valid_block(last_block, block)

def main():
  blockchain = Blockchain()
  blockchain.add_block('one')
  blockchain.add_block('two')

  print(blockchain)


if __name__ == '__main__':
  main()
