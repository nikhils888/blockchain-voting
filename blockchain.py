import hashlib
import json
from time import time
from vote_stats import update_vote_count
import os

class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()

    def create_block(self, voter_hash, vote):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(time()),
            'voter_hash': voter_hash,
            'vote': vote,
            'previous_hash': self.chain[-1]['current_hash'] if self.chain else '0',
            'nonce': 0
        }
        block['current_hash'] = self.hash_block(block)
        self.chain.append(block)
        self.save_chain()
        update_vote_count(vote)
        return block

    def hash_block(self, block):
        block_str = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()

    def save_chain(self):
        os.makedirs('blockchain_data', exist_ok=True)
        with open('blockchain_data/chain.json', 'w') as f:
            json.dump(self.chain, f, indent=2)

    def load_chain(self):
        path = 'blockchain_data/chain.json'
        if os.path.exists(path):
            try:
                with open(path) as f:
                    data = f.read().strip()
                    if not data:
                        raise ValueError("Empty file")
                    self.chain = json.loads(data)
            except (json.JSONDecodeError, ValueError):
                # File is empty or corrupt, create new genesis block
                self.chain = []
                self.create_block(voter_hash="GENESIS", vote="GENESIS")
        else:
            self.create_block(voter_hash="GENESIS", vote="GENESIS")

