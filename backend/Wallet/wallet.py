import uuid
import json

from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

class Wallet:
  """
  An individual wallet for a miner.
  Keeps track of the miner's balance.
  Allows a miner to authorize transactions.
  Standards of Efficient Crypotography Prime 256 bits algorithm
  """

  def __init__(self):
    self.address = str(uuid.uuid4())[0:8]
    self.balance = STARTING_BALANCE
    self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
    self.public_key = self.private_key.public_key()

  def sign(self, data):
    """
    Generates a signature based on the data using the local private key.
    """
    return self.private_key.sign(
      json.dumps(data).encode('utf-8'),
      ec.ECDSA(hashes.SHA256())
    )

  @staticmethod
  def verify(public_key, data, signature):
    """
    Verify a signature based on the original public key and data.
    The public key created from the private key has the built-in verify() method.
    This method returns true if the private key associated with the public key was used to sign the transaction confirming the signature
    and the data has not been tampered with between signing and verification.
    """
    try:
      public_key.verify(
        signature,
        json.dumps(data).encode('utf-8'),
        ec.ECDSA(hashes.SHA256())
      )
      return True
    except InvalidSignature:
      return False

def main():
  wallet = Wallet()
  print(f'Wallet: {wallet.__dict__}')

  data = { 'foo': 'bar'}
  signature = wallet.sign(data)
  print(f'Signature: {signature}')

  should_be_valid = Wallet.verify(wallet.public_key, data, signature)
  print(f'should_be_valid: {should_be_valid}')

  # Should fail as we are creating a different wallet instance and 
  should_be_invalid = Wallet.verify(Wallet().public_key, data, signature)
  print(f'should_be_invalid: {should_be_invalid}')

if __name__ == "__main__":
    main()
