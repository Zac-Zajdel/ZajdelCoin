# ZajdelCoin

### ZajdelCoin is my personal attempt to gain an in-depth understanding of blockchain technology.

##### TODO:

1. Allow For Transaction / Wallets / Keys
2. Connect ZajdelCoin and Blockchain
3. Create Front-end with React, Redux
4. Get real-time data about Bitcoin, Ethereum, etc... from API.
5. Attempt to integrate into HOME repository.

**Activate the virtual machine:**

```
blockchain-env\Scripts\activate.bat
```

**Running the server**

```
python -m backend.app
```

**Run a peer instance**

```
export PEER=True && python -m backend.app
```

**Executing a module**

```
python -m PATH
```

**Install all packages**

```
pip3 install -r requirements.txt
```

**Testing with pytest**

```
python -m pytest backend\tests
```

# Relevant information regarding ZajdelCoin's functonality: 

### What is ZajdelCoin and how does it work?

ZajdelCoin works by having a list of blocks where each block represents a unit of storage for data. The list is called a chain because each block references the block before it, creating (chain) links between blocks. Each block stores a transaction.

### What is the concept of mining blocks?

Mining blocks refers to the process of running a computationally expensive algorithm in order to create new blocks for the blockchain.

### What is the genesis block?

The genesis block is the first block created in ZajdelCoin. Since all blocks must reference the block that came before it, the genesis block serves as a hardcoded starter block for the chain.

### What is the hash value created on every single block?

The hash value is generated by an algorithm that generates a unique output for every input. In the case of this project, we're using the sha-256 algorithm, which produces a unique 256 character hash in binary, and a 64 character hash in hexadecimal.

### What is the Proof of Work concept found in cryptocurrencies?

Proof of work is a mechanism that requires miners to solve a computational puzzle in order to create valid blocks. Solving the puzzle requires a brute-force algorithm that demands CPU power.

### What is the requirement for finding a valid block to add to the chain?

The leading 0's requirement is the standard proof of work implementation for finding valid blocks. By adjusting a nonce value in the block, the miner has an infinite number of tries at generating new hashes. Once the miner finds a hash with a matching number of leading 0's that coincides with the block difficulty level, the fields for valid new block have been found.

### How difficult is it to obtain a valid block to be added to the chain?

Dynamic difficulty is a mechanism that increases or decreases the difficulty of the next block based on how long it takes to mine the new block. If the time is exceeding an established mining rate for the system, the difficulty decreases. Likewise, if the time it took to succcessfully find the leading 0's requirement does not exceed the mine rate, the difficulty increases. This allows ZajdelCoin to control the rate at which blocks are added.

### How does ZajdelCoin ensure that a chain is valid?

Chain validation is the process of ensuring that data of an external chain is formatted correctly. For the chain to be valid, there are multiple rules to enforce. For starters, every block must be valid, with a proper hash based on the block fields, correctly adjusted difficulty, acceptable number of leading 0's in the hash for the proof of work requirement, and more. Likewise, the chain itself must start with the genesis block, and every block's last hash must reference the hash of the block that came before it hence the term "chaining".

### How does ZajdelCoin ensure the validity of a chain before replacing the current chain?

Chain replacement is the process of substituting the current chain data for the data of an incoming chain. If the incoming chain is longer, and valid, then it should replace the current chain. This will allow a valid chain, with new blocks, to spread across the eventual ZajdelCoin network, becoming the true chain that all nodes in the ZajdelCoin network agree upon.

### What is a wallet?

A digital wallet is where a user stores information their money and other items needed to make transaction on the network such as the following:
* Balance - The amount of ZajdelCoin the user owns.
* Private Key - Allows the user to generate unique signature for transactions.
* Public Key - Allows other individuals to verify the signature ensuring not tampering occured with the data.
* Public Address - Allows for other individuals to sent currency to the user.

### What is a transaction?

A transaction occurs when a user sends ZajdelCoin over the network to another user. A transaction contains the following information.
* Input - details about original sender.
* Output - Amount and address.
* Output - The amount the sender should have left and address.

### What are digital signatures?

Digital signatures allow for verification behind a transaction. The public key of the user can be used to decrypt the private key. This allows the receiver to verify the original data was not tampered with and validate the transaction.