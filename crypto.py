import datetime
import json
from flask import Flask,jsonify
import hashlib
from uuid import uuid4
import requests
from urllib.parse import urlparse

class Blockchain:
	def __init__(self):
		self.chain=[]
		self.transaction=[]
		self.nodes=set()
		self.create_block(proof=1,prev_hash='0')

	def create_block(self,proof,prev_hash):
		block={
		'index':len(self.chain)+1,
		'timestamp':str(datetime.datetime.now()),
		'proof':proof,
		'prev_hash':prev_hash,
		'transaction':self.transaction
		}
		self.transaction=[]
		self.chain.append(block)
		return block

	def get_previous_Block(self):
		return self.chain[-1]

	def proof_of_work(self,previous_proof):
		new_proof=1
		check_proof=False
		while check_proof is False:
			hashoperation=hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
			if hashoperation[:4]=='0000':
				check_proof=True
			else:
				new_proof+=1
		return new_proof

							#Watch again
	def hashfunc(self,block):
		encodedBlock=json.dumps(block,sort_keys=True).encode()
		return hashlib.sha256(encodedBlock).hexdigest()

	def isChainValid(self,chain):
		previous_block=chain[0]
		block_index=1
		while block_index < len(chain):
			block=chain[block_index]
			if block['prev_hash'] != self.hashfunc(previous_block):
				return False
			previous_proof=previous_block['proof']
			proof=block['proof']
			hashoperation=hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
			if hashoperation[:4] != '0000':
				return False
			previous_block=block
			block_index+=1
		return True

	def add_transaction(self,sender,receiver,amount):
		self.transaction.append({
			'sender':sender,
			'receiver':receiver,
			'amount':amount
			})
		previous_block=self.get_previous_Block()
		return previous_block['index']+1

	def add_node(self,address):
		parsed_add=urlparse(address)
		self.nodes.add(parsed_add.netloc)

	def replace_chain(self):
		network=self.nodes
		longest_chain=None
		max_length=len(self.chain)
		for node in networks:
			response=requests.get(f'http://{node}/get_chain')
			if response.status_code==200:
				chain=response.json()['chain']
				length=response.json()['length']
				if length > longest_chain and self.isChainValid(chain):
					max_length=length
					longest_chain = chain
		if longest_chain:
			self.chain=longest_chain
			return True
		return False
					

#step 4


# WebApplication Using Flask

app = Flask(__name__)

#Node Address

node=str(uuid4()).replace('-','')

#blockchain instance/object
blockchain=Blockchain()

#mining our block

@app.route('/mine',methods=['GET'])
def mineBlock():
	previousBlock = blockchain.get_previous_Block()
	previous_proof = previousBlock['proof']
	proof = blockchain.proof_of_work(previous_proof)
	previous_hash = blockchain.hashfunc(previousBlock)
	blockchain.add_transaction(sender=node,receiver='bijay',amount=2)
	block = blockchain.create_block(proof,previous_hash)
	response={
	'message':'congratulations you just mined a block!',
	'index': block['index'],
	'timestamp':block['timestamp'],
	'proof':block['proof'],
	'prev_hash':block['prev_hash'],
	'transactions':block['transaction']
	}
	return jsonify(response), 200

#Getting the chain to display
@app.route('/get_chain',methods=['GET'])
def getchain():
	response={
	'chain':blockchain.chain,
	'chain_len':len(blockchain.chain)
	}
	return jsonify(response), 200

@app.route('/chain_valid',methods=['GET'])
def isChainValid():
	chain=blockchain.chain
	validation=blockchain.isChainValid(chain)
	if validation:
		response={
		'message':'Chain is valid'
		}
	else:
		response={
		'message':'not valid'
		}
	return jsonify(response), 200



app.run(host='0.0.0.0',port = 5000)