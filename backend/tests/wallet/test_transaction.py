import pytest

from backend.Wallet.transaction import Transaction
from backend.Wallet.wallet import Wallet

def test_transaction():
  sender_wallet = Wallet()
  recipient = 'recipient'
  amount = 100

  transaction = Transaction(sender_wallet, recipient, amount)

  # Tests variables are going in as expected to init method.
  assert transaction.output[recipient] == amount
  assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount

  # asserts all key value pairs are valid sender_wallet instance variables.
  assert 'timestamp' in transaction.input
  assert transaction.input['amount'] == sender_wallet.balance
  assert transaction.input['address'] == sender_wallet.address
  assert transaction.input['public_key'] == sender_wallet.public_key
  
  # Make sure the wallet is verified with the transaction.
  assert Wallet.verify(
    transaction.input['public_key'],
    transaction.output,
    transaction.input['signature']
  )

def test_transaction_exceeding_balance_of_wallet():
  with pytest.raises(Exception, match="Amount exceeds balance"):
    Transaction(Wallet(), 'recipient', 10000)

def test_transaction_update_exceeds_balance():
  sender_wallet = Wallet()
  transaction = Transaction(sender_wallet, 'recipient', 50)

  with pytest.raises(Exception, match="Amount exceeds balance"):
    transaction.update(sender_wallet, 'new_recipient', 9000)

def test_transaction_update_successful():
  sender_wallet = Wallet()
  first_recipient = 'first_recipient'
  first_amount = 50

  transaction = Transaction(sender_wallet, first_recipient, first_amount)

  next_recipient = 'next_recipient'
  next_amount = 75
  transaction.update(sender_wallet, next_recipient, next_amount)

  assert transaction.output[next_recipient] == next_amount
  assert transaction.output[sender_wallet.address] == sender_wallet.balance - first_amount - next_amount

  # Verifies making an update on a transaction correctly reduces the output inside the transaction class.
  assert Wallet.verify(
    transaction.input['public_key'],
    transaction.output,
    transaction.input['signature']
  )

  # Update going to a recipient that already existed showing that they made two transactions.
  to_first_again_amount = 50
  transaction.update(sender_wallet, first_recipient, to_first_again_amount)

  assert transaction.output[first_recipient] == first_amount + to_first_again_amount
  assert transaction.output[sender_wallet.address] == sender_wallet.balance - first_amount - next_amount - to_first_again_amount

  assert Wallet.verify(
    transaction.input['public_key'],
    transaction.output,
    transaction.input['signature']
  )

def test_valid_transaction():
  Transaction.is_valid_transaction(Transaction(Wallet(), 'recipient', 50))

def test_invalid_transaction_with_invalid_output():
  sender_wallet = Wallet()
  transaction = Transaction(sender_wallet, 'recipient', 50)

  # Tests someone trying to get more money
  transaction.output[sender_wallet.address] = 9999

  with pytest.raises(Exception, match="Invalid transaction output values"):
    Transaction.is_valid_transaction(transaction)

def test_valid_transaction_with_invalid_signature():
  transaction = Transaction(Wallet(), 'recipient', 50)

  # Changing the signature of the transaction input with a valid output but from a different wallet instance.
  transaction.input['signature'] = Wallet().sign(transaction.output)

  with pytest.raises(Exception, match="Invalid Signature"):
    Transaction.is_valid_transaction(transaction)

