# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request, render_template
import requests
from uuid import uuid4
from urllib.parse import urlparse
from markupsafe import escape
import sys
import os

#Blockchain
class Blockchain:

    def __init__(self):
        self.new_block_mined = 0
        self.block_mined_now = 0
        self.chain = []
        self.transactions = []
        self.create_start_block(previous_hash = '0')
        self.nodes = set()
    
    def get_previous_block(self):
        return self.chain[-1]

    def save_chain(self,chain):
        save = {'chain': chain,
                'length': len(chain)}
        f = open ('chain.json', 'w')
        json_save = json.dumps(save)
        f.write(json_save)
        f.close()

    def open_chain(self):
        try:
            f = open('chain.json', 'r')
        except:
            pass
        else:
            chain_json = json.loads(f.read())
            chain = chain_json['chain']
            if self.is_chain_valid(chain):
                self.chain = chain

    def hash(self, block):
        block_ind = str(block['index']).encode('utf-8')
        block_timestamp = str(block['timestamp']).encode('utf-8')
        block_proof = str(block['proof']).encode('utf-8')
        block_phash = str(block['previous_hash']).encode('utf-8')
        block_transactions = str(block['transactions']).encode('utf-8')
        return hashlib.sha256(block_ind + block_timestamp + block_proof + block_phash + block_transactions).hexdigest()
    
    def proof_of_work(self, new_block):
        new_proof = 1
        check_proof = False
        new_block['proof'] = new_proof
        block_ind = str(new_block['index']).encode('utf-8')
        block_timestamp = str(new_block['timestamp']).encode('utf-8')
        block_phash = str(new_block['previous_hash']).encode('utf-8')
        block_transactions = str(new_block['transactions']).encode('utf-8')
        while check_proof is False:
            block_proof = str(new_block['proof']).encode('utf-8')
            hash_operation = hashlib.sha256(block_ind + block_timestamp + block_proof + block_phash + block_transactions).hexdigest()
            if hash_operation[:4] == '0000':
               check_proof = True
            else:
                new_proof += 1
                new_block['proof'] = new_proof
            if self.new_block_mined: 
                return 0
        return new_proof
        
    def create_block(self, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': 0,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        proof = self.proof_of_work(block)
        self.transactions = []        
        if proof == 0:
            self.new_block_mined = 0
            self.block_mined_now = 0
            return 0
        else:
            self.new_block_mined = 0            
            self.chain.append(block)
            print(f'I find Block {proof}')
            self.block_mined_now = 0  
            network = self.nodes
            o = urlparse(request.base_url)
            hostname_cur = o.hostname + ':' + str(o.port)        
            for node in network:
                if node != hostname_cur:
                    try:
                        requests.get(f'http://{node}/new_block_is_mined', timeout=0.1)
                    except :
                        pass
            self.replace_chain()
            self.save_chain(self.chain)
            return block
        
    def create_start_block(self, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': 1,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.proof_of_work(block)
        self.new_block_mined = 0
        self.transactions = []
        self.chain.append(block)
        return block
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            hash_operation = self.hash(previous_block)
            if block['previous_hash'] != hash_operation:
                print(f'Alarm blocks {block_index} not valid {hash_operation}\r\n{chain}')
                return False
            if hash_operation[:4] != '0000':
                print(f'Alarm blocks {block_index} not valid0000 {hash_operation}\r\n{chain}')
                return False
            previous_block = block
            block_index += 1
        return True
    
    def add_transaction(self, sender, receiver, message, signature):
        for transaction in self.transactions:
            if  transaction['sender'] == sender and \
                transaction['receiver'] == receiver and \
                transaction['message'] == message and \
                transaction['signature'] == signature:
                return 0
        self.transactions.append({'message': message,
                                  'receiver': receiver,
                                  'sender': sender,
                                  'signature': signature})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        for node in self.nodes:
            if node == parsed_url.path:
                return
        self.nodes.add(parsed_url.path)
    
    def replace_chain(self):
        network = self.nodes
        o = urlparse(request.base_url)
        hostname_cur = o.hostname + ':' + str(o.port)        
        longest_chain = None
        max_length = len(self.chain)
        min_proof = self.chain[-1]['proof']
        for node in network:
            if node != hostname_cur:
                try:
                    response = requests.get(f'http://{node}/get_chain', timeout=0.1)
                except: 
                    pass
                else:
                    if response.status_code == 200:
                        length = response.json()['length']
                        chain = response.json()['chain']
                        if length == max_length and min_proof  > chain[-1]['proof']:
                            min_proof = chain[-1]['proof']
                            longest_chain = chain
                        if length > max_length and self.is_chain_valid(chain):
                            max_length = length
                            min_proof = chain[-1]['proof']
                            longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            self.save_chain(self.chain)
            print('Chain replaced for New')
            return True
        print('Chain None replaced')
        return False

    def parse_signatures(self,chain):
        signatures_list = []
        for zv in chain:
            transactions = zv['transactions']
            for transction in transactions:
                new_signature = transction['signature']
                signature_pref = 0
                for signature in signatures_list:
                    if signature == new_signature:
                        signature_pref = 1
                        break
                if signature_pref == 0:
                    signatures_list.append(transction['signature'])
        return signatures_list
    
    def parse_signature_transaction(self,chain, signature):
        transactions_list = []
        for zv in chain:
            transactions = zv['transactions']
            for transction in transactions:
                if signature == transction['signature']:
                    transactions_list.append(transction)
        return transactions_list
    
#HTTP 
app = Flask(__name__)
node_address = str(uuid4()).replace('-', '')
print(f'Node adress: {node_address}')
blockchain = Blockchain()

@app.route('/')
def get_main_form():
    try:
        f = open('templates/index.html', 'r')
    except:
        return '404', 404
    else:
        f.close()
        return render_template('index.html'), 200

@app.route('/parse_signatures')
def parse_signatures():
    signatures = blockchain.parse_signatures(blockchain.chain)
    response = {'signatures': list(signatures)}
    return jsonify(response),200

@app.route('/parse_transactions/<signature>')
def parse_transactions(signature):
    transactions = blockchain.parse_signature_transaction(blockchain.chain,escape(signature))
    response = {'transactions': list(transactions)}
    return jsonify(response),200

@app.route('/new_block_is_mined', methods = ['GET'])
def new_block_is_mined():
    blockchain.new_block_mined = 1;
    response = {'message': 'Block Stopped'}
    blockchain.replace_chain()    
    return jsonify(response), 200

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    if len(blockchain.transactions) > 0:
        if blockchain.block_mined_now == 0:
            blockchain.block_mined_now = 1
            blockchain.new_block_mined = 0
            network = blockchain.nodes
            o = urlparse(request.base_url)
            hostname_cur = o.hostname + ':' + str(o.port)  
            for node in network:
                if node != hostname_cur:
                    try:
                        response = requests.get(f'http://{node}/mine_block', timeout=0.0000000001)
                    except:
                        pass
            previous_block = blockchain.get_previous_block()
            previous_hash = blockchain.hash(previous_block)
            block = blockchain.create_block(previous_hash)
            if block == 0:
                block = blockchain.get_previous_block()
            response = {'message': 'Блок найден!',
                            'index': block['index'],
                            'timestamp': block['timestamp'],
                            'proof': block['proof'],
                            'previous_hash': block['previous_hash'],
                            'transactions': block['transactions']}
            return jsonify(response), 200    
        else:
            print ('Mining is progress')
            response = {'message': 'Блок майнится!'}
            return jsonify(response), 400
    else:
        response = {'message': 'В сети нет транзакций!'}
        return jsonify(response), 200
    
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/get_chain_json')
def get_chain_json():
    f = open('chain.json', 'r')
    html = f.read()
    f.close()
    return html, 200

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'Блокчейновая цепочка верна.'}
    else:
        response = {'message': 'Блокчейновая цепочка НАРУШЕНА.'}
    return jsonify(response), 200

@app.route('/add_transaction', methods = ['GET'])
def add_transaction():
    jsonp = request.get_json()
    transaction_keys = ['sender', 'receiver', 'message', 'signature']
    if not all(key in jsonp for key in transaction_keys):
        return 'Форма транзакции неверна', 400
    index = blockchain.add_transaction(jsonp['sender'], jsonp['receiver'], jsonp['message'], jsonp['signature'])
    if index != 0:
        network = blockchain.nodes
        o = urlparse(request.base_url)
        hostname_cur = o.hostname + ':' + str(o.port)        
        headers = {'Content-type': 'application/json',  
           'Accept': 'text/plain',
           'Content-Encoding': 'utf-8'}
        for node in network:
            if node != hostname_cur:
                try:
                    requests.get(f'http://{node}/add_transaction', data = json.dumps(jsonp), headers=headers, timeout=0.0000000001)
                except:
                    pass
        response = {'message': f'Транзакция учтена и предположительно будет проведена в блоке {index}'}
        return jsonify(response), 200
    else:
        response = {'message': 'Транзакция имеется в пуле'}
        return jsonify(response), 400
    
@app.route('/sync_transactions', methods = ['GET'])
def sync_transaction():
    return jsonify(list(blockchain.transactions)), 200

@app.route('/connect_nodes', methods = ['GET'])
def connect_nodes():
    jsonp = request.get_json()
    nodes = jsonp.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'Все узлы учтены. Блокчейн содержит следующие узлы:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 200

@app.route('/get_nodes', methods = ['GET'])
def get_nodes():
    response = {'nodes': list(blockchain.nodes)}
    return jsonify(response), 200

@app.route('/add_node', methods = ['GET'])
def add_node():
    jsonp = request.get_json()
    node = jsonp.get('nodes')
    blockchain.add_node(node)
    f = open('nodes.json','w')
    nodes_list = {'nodes': list(blockchain.nodes),
                  'length': len(blockchain.nodes)}
    json_node_list = json.dumps(nodes_list)
    f.write(json_node_list)
    f.close()
    return jsonify(list(blockchain.nodes)), 200

@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'Другой узел содержит более новую цепь. Замена блокчейновой цепочки.',
                    'new_chain': blockchain.chain}
        print('New blockchain valid')
    else:
        response = {'message': 'Текущая блокчейновая цепочка верна.',
                    'actual_chain': blockchain.chain}
        print('Current blockchain valid')
    return jsonify(response), 200

#Получение списка узлов
print('Create folder "templates"')
try:
    os.mkdir("templates")
except:
    pass

print('Open nodes file')
try:
    f = open('nodes.json','r')
except:
    pass
else:
    jsonp = json.loads(f.read())
    f.close()
    nodes = jsonp.get('nodes')
    for node in nodes:
            blockchain.add_node(node)

print('Open chain file')
blockchain.open_chain()

port_node = 5000
host_node = '127.0.0.1'
arg = sys.argv
if arg:
    if len(arg) > 1:
        port_node = arg[1]
    if len(arg) > 2:
        host_node = arg[2]
    
print(f'Node start on {host_node} to port: {port_node}')

print('Try to connect nodes')
hostname_cur = '127.0.0.1' + ':' + str(port_node)  
blockchain.add_node(hostname_cur)
network = blockchain.nodes
headers_main = {'Connection': 'close'}
for net_node in network:
    if net_node != hostname_cur:
        try:
            response = requests.get(f'http://{net_node}/get_nodes',headers=headers_main) 
        except:
            pass
        else:
            print(f'Node {net_node} is active. Syncronization...')
            response.close()
            nodes = response.json()['nodes']            
            if nodes is None:
                pass
            else:
                net_node_have_me = 0
                for node in nodes:
                    blockchain.add_node(node) 
                    if node == hostname_cur:
                        net_node_have_me = 1
                if net_node_have_me == 0:
                    message = {'nodes': hostname_cur,
                               'lentgth': 1}
                    headers = {'Content-type': 'application/json',  
                       'Accept': 'text/plain',
                       'Content-Encoding': 'utf-8',
                       'Connection': 'close'}
                    data = json.dumps(message)
                    print(f'Try to response node {net_node}')
                    try:
                        response = requests.get(f'http://{net_node}/add_node', data=data, headers=headers) 
                    except:
                        pass
                    else:
                        response.close()

# Запуск сервера
print('Node ready to start:')
app.run(host = host_node, port = port_node)
