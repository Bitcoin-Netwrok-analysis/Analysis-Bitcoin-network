import json
import matplotlib.pyplot as plt
user_list = []
import numpy as np

CRIMINAL = 0
EXCHANGE = 1
MINER = 2
SERVICES = 3

class User:
    
    def __init__(self, address,total_out_degree,total_in_degree,blocks,transaction_sent, transaction_received,tag):
        self.address = address
        self.total_out_degree = total_out_degree
        self.total_in_degree = total_in_degree
        self.blocks = blocks
        self.transaction_sent = transaction_sent 
        self.transaction_received = transaction_received
        self.tag = tag
        
    def to_dict(self):
        return {'address': self.address,
                'total_out_degree': self.total_out_degree,
                'total_in_degree' : self.total_in_degree,
                'blocks' : self.blocks, 
                'transaction_sent' : self.transaction_sent, 
                'transaction_received' : self.transaction_received, 
                'tag' : self.tag
                }

with open('3rd_approach.json') as f:
    for line in f:
        user_dict = json.loads(line)
        if user_dict['total_out_degree']>0 or user_dict['total_in_degree']>0:
            user_list.append(User(user_dict['address'],user_dict['total_in_degree'],user_dict['total_out_degree'],user_dict['blocks'],user_dict['transaction_sent'], user_dict['transaction_received'],user_dict['tag']))

def three_attribute():
    y_crime = []
    y_exchange = []
    y_miner = []
    y_services = []
    x_crime = []
    x_exchange = []
    x_miner = []
    x_services = []
    z_crime = []
    z_exchange = []
    z_miner = []
    z_services = []
    for i in user_list:
        i:User
        match i.tag:
            case 0:
                x_crime.append(np.log2(i.transaction_sent+1))
                y_crime.append((max(i.blocks)-min(i.blocks))/len(i.blocks))
                z_crime.append(np.log2(len(i.blocks)))
                
            case 1:
                if(len(x_exchange)>100):
                    continue
                x_exchange.append(np.log2(i.transaction_sent+1))
                y_exchange.append((max(i.blocks)-min(i.blocks))/len(i.blocks))
                z_exchange.append(np.log2(len(i.blocks)))
                
                
            case 2:
                x_miner.append(np.log2(i.transaction_sent+1))
                y_miner.append((max(i.blocks)-min(i.blocks))/len(i.blocks))
                z_miner.append(np.log2(len(i.blocks)))
                
            
            case 3:
                x_services.append(np.log2(i.transaction_sent+1))
                y_services.append((max(i.blocks)-min(i.blocks))/len(i.blocks))
                z_services.append(np.log2(len(i.blocks)))
                
    fig = plt.figure(figsize = (10,10))
    ax = plt.axes(projection='3d')
    ax.grid()

    ax.scatter(x_crime, y_crime, z_crime, c = 'r') 
    ax.scatter(x_exchange, y_exchange, z_exchange, c = 'b')       
    ax.scatter(x_miner, y_miner, z_miner, c = 'y')       
    ax.scatter(x_services, y_services, z_services, c = 'g')       

    plt.show()

def one_attribute():
    x = []
    y = []

    counter = 0
    for i in user_list:
        i:User
        if i.tag ==0:
            x.append(counter)
            y.append(np.log2(max(i.blocks)-min(i.blocks)+1))
            counter+=1
    print('criminal',counter)
    for i in user_list:
        i:User
        if counter>175:
            break
        if i.tag ==1:
            x.append(counter)
            y.append(np.log2(max(i.blocks)-min(i.blocks)+1))
            counter+=1
    print('exchange',counter)
    for i in user_list:
        i:User
        if i.tag ==2:
            x.append(counter)
            y.append(np.log2(max(i.blocks)-min(i.blocks)+1))
            counter+=1
    print('miner',counter)
    for i in user_list:
        i:User
        if i.tag ==3:
            x.append(counter)
            y.append(np.log2(max(i.blocks)-min(i.blocks)+1))
            counter+=1
    print('services',counter)
    
    plt.scatter(x,y)
    plt.show()
    
one_attribute()
        