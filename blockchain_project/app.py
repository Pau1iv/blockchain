from flask import Flask, request, jsonify
from blockchain import Blockchain
import time

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    """Returns the full blockchain."""
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return jsonify({"length": len(chain_data), "chain": chain_data})

@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    """Mines a new block with unconfirmed transactions."""
    result = blockchain.mine()
    if not result:
        return jsonify({"message": "No transactions to mine"}), 400
    return jsonify({"message": f"Block #{result} is mined."}), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """Adds a new transaction to the list of unconfirmed transactions."""
    tx_data = request.get_json()
    required_fields = ["sender", "receiver", "data", "balance"]

    for field in required_fields:
        if field not in tx_data:
            return "Invalid transaction data", 404

    tx_data["timestamp"] = time.time()
    blockchain.add_new_transaction(tx_data)
    return "Success", 201

@app.route('/wallet/<address>', methods=['GET'])
def get_wallet(address):
    """Returns the balance of a given wallet address."""
    balance = 0
    for block in blockchain.chain:
        for transaction in block.transactions:
            if transaction['sender'] == address:
                balance -= int(transaction['balance'])
            if transaction['receiver'] == address:
                balance += int(transaction['balance'])
    response = {'address': address, 'balance': balance}
    return jsonify(response), 200

@app.route('/valid', methods=['GET'])
def validate_chain():
    """Validates the integrity of the blockchain."""
    valid = blockchain.is_chain_valid(blockchain.chain)
    response = {'is_valid': valid}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
