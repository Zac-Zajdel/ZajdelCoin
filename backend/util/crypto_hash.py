import hashlib
import json


def crypto_hash(*args):
  """
  Return a sha-256 hash of the given arguments.
  """
  stringified_args = sorted(map(lambda data: json.dumps(data), args))
  joined_data = ''.join(stringified_args)

  return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()


def main():
  # Demonstrates that regardless of how many items added/position, the same hash value is created.
  print(f"crypto_hash: {crypto_hash('one', '2', [3])}")
  print(f"crypto_hash: {crypto_hash('one', [3], '2')}")


if __name__ == '__main__':
  main()
