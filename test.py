import datetime
import json
import hashlib
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse


class Blockchain:
	def __init__(self):
		self.chain=[]
		self.transactions=[]
		self.create_block(proof=1, prev_hash='0')
		self.nodes=set()

	def create_block(self,proof,prev_hash):
		block={
		'index':len(self.chain)+1,
		'timestamp':str(datetime.datetime.now()),
		'proof':proof,
		'prev_hash':prev_hash,
		'transactions':self.transactions
		}
		self.transactions=[]
		self.chain.append(block)
		return block

	def get_previous_Block(self):
		return self.chain[-1]


	def proof_of_work(self,previous_proof):
		new_proof=1
		check_proof=False
		while check_proof is False:
			hashed=hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
			if hashed[:4]=='0000':
				check_proof=True
			else:
				new_proof+=1
		return new_proof

	def hash_func(self,block):
		hashed_function=json.dumps(block).encode()
		return hashlib.sha256(hashed_function).hexdigest()

	def is_chain_valid(self,chain):
		previous_block=chain[0]
		block_index=1
		while block_index < len(chain):
			block=chain[block_index]
			if block['prev_hash']!= hash_func(previous_block):
				return False
			previous_proof=previous_block['proof']
			new_proof=block['proof']
			hashoperation=hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
			if hashoperation[:4]!='0000':
				return False
			previous_block=block
			block_index+=1
		return True

	def add_transactions(self,sender,receiver,amount):
		self.transactions.append({
			'sender':sender,
			'receiver':receiver,
			'amount':amount
			})
		previous_block=self.get_previous_Block()
		return previous_block['index']+1

	def add_nodes(self,address):
		parsed_address=urlparse(address)
		return self.nodes.add(parsed_address.netloc)

	def replace_chain(self):
		network=self.nodes
		longest_chain=None
		max_length=len(self.chain)
		for node in networks:
			response=requests.get(f'http://{node}/get_chain')
			if response.status_code==200:
				length=response['length']
				chain=response['chain']
				if length > max_length and self.is_chain_valid(chain):
					longest_chain=chain
					max_length=length
		if longest_chain:
			self.chain=longest_chain
		return False				


#Mining a block
app=Flask(__name__)
node_address=str(uuid4()).replace('-','')

blockchain=Blockchain()
@app.route('/mine',methods=['GET'])
def mine():
	previous_block=blockchain.get_previous_Block()
	previous_proof=previous_block['proof']
	proof=blockchain.proof_of_work(previous_proof)
	previous_hash=blockchain.hash_func(previous_block)
	blockchain.add_transaction(sender=node_address,receiver='vijay',amount=2)
	block=blockchain.create_block(proof,previous_hash)
	response={
	'message':'Congratulations you have successfully mined a block',
	'index':block['index'],
	'timestamp':block['timestamp'],
	'proof':block['proof'],
	'previous_hash':block['prev_hash'],
	'transaction':block['transactions']
	}
	return jsonify(response), 200

@app.route('/get_chain',methods=['GET'])
def get_chain():
	chain=blockchain.chain
	length=len(chain)
	response={
	'chain':chain,
	'length':length
	}
	return jsonify(response), 200

@app.route('/is_chain_valid',methods=['GET'])
def is_chain_valid():
	is_valid=blockchain.is_chain_valid(blockchain.chain)
	if is_valid:
		response={"message":"The chain is perfectly valid"}
	else:
		response={"message":"The chain seems to be invalid!"}
	return jsonify(response),200



@app.route('/add_transaction',method=['POST'])
def add_transaction():
	json=request.get_json()
	transaction_key=['sender','receiver','amount']
	if not all(key in json for key in transaction_key):
		return 'some of the transaction fields are missing :(', 400
	index=blockchain.add_transaction(sender=json['sender'],receiver=json['receiver'],amount=json['amount'])
	response={"message":f'the transactions will be added in block no. {index}'} 
	return jsonify(response), 201

@app.route('/add_node',methods=['POST'])
def add_node():
	json=request.get_json()
	nodes=json['nodes']
	if nodes is None:
		return 'No nodes',400
	for node in nodes:
		blockchain.add_nodes(node)
	response={
	'message':'Yay you are up added',
	'total nodes': list(blockchain.nodes)
	}
	return jsonify(response),201

@app.route('/replace_chain',methods=['GET'])
def replace_chain():
	is_chain_replaced=blockchain.replace_chain(blockchain.chain)
	if is_chain_replaced:
		response={"message":"The chain is Replaced",
				  "new chain":blockchain.chain}
	else:
		response={"message":"The chain is perfect"}
	return jsonify(response),200



app.run(host='0.0.0.0',port=5001)