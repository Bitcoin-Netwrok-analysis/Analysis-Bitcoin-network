import threading
import requests
import csv
import json
import time

CRIMINAL=0
EXCHANGE = 1
MINER = 2
SERVICES = 3

def hash_fun(para):
    return abs(hash(para))%50

class User:
    
    def __init__(self, address):
        self.address = address
        self.total_out_degree = 0 
        self.total_in_degree = 0 
        self.blocks = []
        self.transaction_sent = 0 
        self.transaction_received = 0 
        self.tag = None
        
    def to_dict(self):
        return {'address': self.address,
                'total_out_degree': self.total_out_degree,
                'total_in_degree' : self.total_in_degree,
                'blocks' : self.blocks, 
                'transaction_sent' : self.transaction_sent, 
                'transaction_received' : self.transaction_received, 
                'tag' : self.tag
                }
        
        
user_list = {}
NUM =100000000
threads = []
block_hashes = 0
n = 0
locks = []

def Worker(s,e):
        
    for i in range(s,e+1):
        print(i,end='\r')
        hashy = block_hashes[i] 
        url = f'https://blockchain.info/rawblock/{hashy}'
        try:
            response = requests.get(url).json()
        except:
            print(1)
            continue
        block_index = response['block_index']
        
        for j in response['tx']:
            inputs_values = {}
            output_values = {}
            inputs = j['inputs']
            outputs = j['out']
            for k in inputs:
                if 'addr' in k['prev_out']:
                    if k['prev_out']['addr'] in inputs_values:
                        inputs_values[k['prev_out']['addr']]+= (k['prev_out']['value']/NUM)    
                    else:
                        inputs_values[k['prev_out']['addr']]= (k['prev_out']['value']/NUM)    
            for k in outputs :
                if 'addr' in k:
                    if k['addr'] in output_values:
                        output_values[k['addr']]+= k['value']/NUM   
                    else:
                        output_values[k['addr']]= k['value']/NUM 
            for k in inputs_values:
                if not (k in user_list):
                    continue
                locks[hash_fun(k)].acquire()
                user:User = user_list[k]
                user.total_in_degree+=1
                if k in output_values:
                    user.transaction_sent+=abs(inputs_values[k]-output_values[k])
                else:
                    user.transaction_sent+=(inputs_values[k])
                if not (block_index in user.blocks):
                    user.blocks.append(block_index)
                locks[hash_fun(k)].release()
                
            for k in output_values:
                if not (k in user_list):
                    continue
                locks[hash_fun(k)].acquire()
                user:User = user_list[k]
                if not (k in inputs_values):
                    user.total_out_degree+=1                
                    user.transaction_received+=abs(output_values[k])
                    if not (block_index in user.blocks):
                        user.blocks.append(block_index)
                locks[hash_fun(k)].release()
                
           
        
            
if __name__=='__main__':
    with open('tag.csv', mode = 'r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            if len(row)==0: continue
            user_list[row[0]] = User(row[0]) 
            user:User = user_list[row[0]]
            if(row[1]==''):
                user.tag = CRIMINAL
            else:
                match row[1]:
                    case 'miner':
                        user.tag = MINER
                    case 'exchange':
                        user.tag = EXCHANGE
                    case 'user':
                        user.tag = EXCHANGE
                    case default:
                        user.tag = SERVICES

    for i in range(50):
        locks.append(threading.Lock())
    
    with open('hashes.json','r') as f:
        block_hashes = json.load(f)['data']
    threads = []
    
    n = len(block_hashes)
    # n = 1000 
    sum = n//30-1                 
    s =0
    for i in range(31):
        e = n-1
        if(i!=30):
            e = s +sum
        threads.append(threading.Thread(target=Worker, args=(s,e)))
        threads[-1].start()
        s = e+1

    for i in threads:
        i.join()
            
    
    with open('3rd_approach.json', 'w') as f:
        for i in user_list:        
            user = user_list[i]
            user_dict = user.to_dict()
            json.dump(user_dict, f)
            f.write('\n') 