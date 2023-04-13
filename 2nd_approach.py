from threading import Thread
import requests
import csv
import json
import time

CRIMINAL=0
EXCHANGE = 1
MINER = 2
SERVICES = 3

class User:
    
    def __init__(self, address):
        self.address = address
        self.total_out_degree = 0 #done
        self.total_in_degree = 0 #done
        self.prev_block = None #done
        self.block_count = 0 #done
        self.life = None #done
        self.transaction_sent = 0 #done
        self.transaction_received = 0 #done
        self.balance = 0 #done
        self.tag = None
        
    def to_dict(self):
        return {'address': self.address,
                'total_out_degree': self.total_out_degree,
                'total_in_degree' : self.total_in_degree,
                'block_count' : self.block_count, #done
                'life' : self.life, #done
                'transaction_sent' : self.transaction_sent, #done
                'transaction_received' : self.transaction_received, #done
                'balance' : self.balance, #done
                'tag' : self.tag
                }
        
        
user_list = []
NUM =100000000

def Worker(s,e):
    for pointer in range(s,e+1):
        user:User = user_list[pointer]
        address = user.address    
        for i in range(2):    
            num = i*100
            print(pointer,end='\r')
            url = f'https://blockchain.info/multiaddr?active={address}&offset={num}'
            response = requests.get(url).json()
            time.sleep(1)
            
            if i==0:
                user.transaction_sent = response['addresses'][0]['total_sent']/NUM
                user.transaction_received = response['addresses'][0]['total_received']/NUM
                user.balance = response['addresses'][0]['final_balance']/NUM
            txs = response['txs']
            for j in txs:
                if user.prev_block ==None:
                    user.prev_block = j['block_height']
                    user.life = 0
                    user.block_count = 1
                if j['block_height']==user.prev_block:
                    user.block_count+=1
                    user.life+=abs(j['block_height']-user.prev_block)
                    user.prev_block = j['block_height']
                inputs = j['inputs']
                is_input = False
                for k in inputs:
                    if('addr' in k['prev_out'] and k['prev_out']['addr']==user.address):
                        user.total_out_degree+=1
                        is_input = True
                        break
                if is_input:
                    continue
                outputs = j['out']
                for k in outputs:
                    if('addr' in k and k['addr']==user.address):
                        user.total_in_degree+=1
                        break
            if len(txs)<100:
                break
            
def Worker2(s,e):
    for pointer in range(s,e):
        print(pointer,end='\r')
        user:User = user_list[pointer]
        address = user.address
        url = f'https://chain.api.btc.com/v3/address/{address}'
        response = requests.get(url).json()['data']
        user.transaction_sent = response['sent']
        user.transaction_received = response['received']
        user.balance = response['balance']
        user.total_in_degree = response['tx_count']
        
        
            
if __name__=='__main__':
    with open('tag.csv', mode = 'r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            if len(row)==0: continue
            user_list.append(User(row[0]))
            user:User = user_list[-1]
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
    
    n = len(user_list)
    threads = []
    sum = n//50-1
    s = 0
    for i in range(51):
        t = 0
        if i != 50:
            t = Thread(target= Worker, args = (s,s+sum))
        else:
            t= Thread(target=Worker, args = (s,n-1))
        threads.append(t)
        t.start()
        s = s+sum+1
    for i in threads:
        i.join()

    
    with open('2nd_approach.json', 'w') as f:
        for i in range(len(user_list)):        
            user = user_list[i]
            user_dict = user.to_dict()
            json.dump(user_dict, f)
            f.write('\n') 
        
        
        
        
                        
            
        
    
                
                    
                    
                
                
    