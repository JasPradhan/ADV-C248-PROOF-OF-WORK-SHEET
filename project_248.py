import hashlib
import json
from time import time


class Block(object):
    def __init__(self):
        self.chain = []
        self.new_transactions = []
        self.count = 0
        self.new_block(previous_hash="No previous Hash. Since this is the first block.", proof=432)  # Task 01 - Change the value of Proof

    def new_block(self, proof, previous_hash=None):
        block = {
            'Block No': self.count, 
            'timestamp': time(),
            'transactions': self.new_transactions or 'No Transactions First Genesis Block',
            'gasfee': 0.1,
            'nonce': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.new_transactions = []
        self.count = self.count + 1
        self.chain.append(block)

        return block

    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof_condition = False

        while check_proof_condition is False:
            compare_proof = new_proof ** 2 - previous_proof ** 2
            string_compare_proof = str(compare_proof).encode()
            encode_proof = hashlib.sha256(string_compare_proof)
            hash_proof = encode_proof.hexdigest()
            #print('Getting proof of work:',hash_proof)
            if hash_proof[:2]=='00':# Task-02 - Write the if condition here:
                check_proof_condition = True
            else:
                    new_proof = new_proof + 1

        return new_proof

    def transaction(self, sender, recipient, amount):
        sender_encoder = hashlib.sha256(sender.encode())
        sender_hash = sender_encoder.hexdigest()
        recipient_encoder = hashlib.sha256(recipient.encode())
        recipient_hash = recipient_encoder.hexdigest()

        transaction_data = {
            'sender': sender_hash,
            'recipient': recipient_hash,
            'amount': amount
        }
        self.new_transactions.append(transaction_data)
        return self.last_block

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()
        block['Current hash'] = hex_hash
        return hex_hash



blockchain = Block()
transaction1 = blockchain.transaction("Satoshi", "Mike", '5 ETH')
transaction2 = blockchain.transaction("Mike", "Satoshi", '1 ETH')
transaction3 = blockchain.transaction("Satoshi", "Hal Finney", '5 ETH')

previous_block = blockchain.last_block()
print('our previous block:',previous_block)

previous_proof = previous_block['nonce']
print('Previous block proof:',previous_proof)

proof = blockchain.proof_of_work(previous_proof)
print("Found proof of work at:",proof)

previous_hash = blockchain.hash(previous_block)
print('Previous block hash:',previous_hash)

block = blockchain.new_block(proof, previous_hash)

print("Data of blockchain:",blockchain.chain)

# Task 03- Write the if else condition from below
if blockchain.chain[0]['Current hash']==blockchain.chain[1]['previous_hash']:
    print("Proof of work is valid! :)")
else:
    print("Proof of work is not valid :(")

