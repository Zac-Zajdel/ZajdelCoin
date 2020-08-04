import uuid

class Transaction:
  """
  Document the exchange of currency from a sender to one or more recipients
  sender_wallet - Instance of the wallet class.
  recipient - Another wallet's address string.
  amount - The amount of currency exchanged within the transaction.
  """

  def __init__(self, sender_wallet, recipient, amount):
    self.id = str(uuid.uuid4())[0:8]
    self.output = self.create_output(sender_wallet, recipient, amount)
    self.input = self.create_input(sender_wallet, self.output)

  def create_output(self, sender_wallet, recipient, amount):
    """
    Structures the output data for the transaction.
    """
    if amount > sender_wallet.balance:
      raise Exception('Amount exceeds balance')
    output = {}
    output[recipient] = amount
    output[sender_wallet.address] = sender_wallet.balance - amount

    return output

  def create_input(self, sender_wallet, output):
    return True
