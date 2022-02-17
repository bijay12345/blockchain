import datetime
import json
from flask import Flask,jsonify
import hashlib

class Blockchain:
	def __init__(self):
		self.chain=[]
		self.create_block(proof=1,prev_hash='0')

	def create_block(self,proof,prev_hash):
		block={
		'index':len(self.chain)+1,
		'timestamp':str(datetime.datetime.now()),
		'proof':proof,
		'prev_hash':prev_hash,
		}
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
			if block['prev_hash'] != hashfunc(previous_block):
				return False
			previous_proof=previous_block['proof']
			proof=block['proof']
			hashoperation=hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
			if hashoperation[:4] != '0000':
				return False
			previous_block=block
			block_index+=1
		return True




# WebApplication Using Flask

app = Flask(__name__)

blockchain=Blockchain()

#mining our block

@app.route('/mine',methods=['GET'])
def mineBlock():
	previousBlock = blockchain.get_previous_Block()
	previous_proof = previousBlock['proof']
	proof = blockchain.proof_of_work(previous_proof)
	previous_hash = blockchain.hashfunc(previousBlock)
	block = blockchain.create_block(proof,previous_hash)
	response={
	'message':'congratulations you just mined a block!',
	'index': block['index'],
	'timestamp':block['timestamp'],
	'proof':block['proof'],
	'prev_hash':block['prev_hash'],
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

app.run(host='0.0.0.0',port = 5000)