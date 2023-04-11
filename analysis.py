from enum import Enum
import csv
import json
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np


class Tag(Enum):
    CRIMINAL = 0
    EXCHANGE = 1
    SERVICES = 2
    MINER = 3
    UNTAGGED = 4
    

class user:
    
    def __init__(self, user_id, out_id,in_id, in_degree_days, out_degree_days,shortest_path,lock =None):
        self.lock = lock
        self.user_id = user_id
        self.out_id = out_id
        self.in_id = in_id
        self.in_degree_days = in_degree_days
        self.out_degree_days = out_degree_days
        self.shortest_path = shortest_path
        self.tag = Tag.UNTAGGED
        
        
    def to_dict(self):
        return {'user_id': self.user_id,
                'out_id': self.out_id,
                'in_id': self.in_id,
                'in_degree_days': self.in_degree_days,
                'out_degree_days': self.out_degree_days,
                'shortest_path': self.shortest_path }
        
    def avg_out_transaction(self):
        if(len(self.out_degree_days)==0): return 0
        ans =0 
        for i in self.out_id:
            ans+=self.out_id[i]
        ans /= (len(self.out_degree_days))
        return ans
    
    def avg_in_transaction(self):
        if(len(self.in_degree_days)==0): return 0
        ans =0 
        for i in self.in_id:
            ans+=self.in_id[i]
        ans /= (len(self.in_degree_days))
        return ans
    
    def avg_indegree_day(self):
        if(len(self.in_degree_days)==0): return 0
        ans =0 
        for i in self.in_degree_days:
            ans+=self.in_degree_days[i]
        ans /= (len(self.in_degree_days))
        return ans
    
    def avg_outdegree_day(self):
        if(len(self.out_degree_days)==0): return 0
        ans =0 
        for i in self.out_degree_days:
            ans+=self.out_degree_days[i]
        ans /= (len(self.out_degree_days))
        return ans
    
    def frequency(self):
        if(len(self.out_degree_days)<=1): return 40
        temp = []
        for i in self.out_degree_days:
            temp.append(int(i))
        temp.sort()
        sum = 0
        for i in range(1,len(temp)):
            sum+=(temp[i]-temp[i-1])
        return sum/(len(temp)-1)
        
            
    
if __name__ == '__main__':
    tags = {}
    with open('tag.csv', mode = 'r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            if len(row)==0: continue
            if(row[1]==''):
                tags[row[0]] = Tag.CRIMINAL
            else:
                match row[1]:
                    case 'miner':
                        tags[row[0]] = Tag.MINER
                    case 'exchange':
                        tags[row[0]] = Tag.EXCHANGE
                    case 'user':
                        tags[row[0]] = Tag.EXCHANGE
                    case default:
                        tags[row[0]] = Tag.SERVICES
    print('process 1 completed')
                
    users = {}
    with open('cluster.csv',mode='r') as file:
        reader = csv.reader(file)
        criminals = 0
        for row in reader:
            if(row[0] in tags):          
                row[1] = int(row[1])
                if(((row[1] in users) and users[row[1]]!=Tag.CRIMINAL) or (not (row[1] in users))):
                    users[row[1]] = tags[row[0]]
    del tags
    print('process 2 completed')
    
                
             
    final_users = []
    with open('last.json', 'r') as f:
        counter = 0
        for line in f:
            user_dict = json.loads(line)
            if counter in users:
                User = user(user_dict['user_id'], user_dict['out_id'], user_dict['in_id'], user_dict['in_degree_days'],user_dict['out_degree_days'],user_dict['shortest_path'])
                User.tag = users[counter]
    
                final_users.append(User)
            counter+=1
    del users
    print('process 3 completed')
    
    
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
    for i in final_users:
        match i.tag:
            case Tag.CRIMINAL:
                x_crime.append(i.frequency())
                y_crime.append(np.log2(i.avg_out_transaction()))
                z_crime.append(np.log2(i.avg_outdegree_day()+1))
                
            case Tag.EXCHANGE:
                if(len(x_exchange)>30):
                    continue
                x_exchange.append(i.frequency())
                y_exchange.append(np.log2(i.avg_out_transaction()))
                z_exchange.append(np.log2(i.avg_outdegree_day()+1))
                
                
            case Tag.MINER:
                x_miner.append(i.frequency())
                y_miner.append(np.log2(i.avg_out_transaction()))
                z_miner.append(np.log2(i.avg_outdegree_day()+1))
                
                
            case Tag.SERVICES:
                x_services.append(i.frequency())
                y_services.append(np.log2(i.avg_out_transaction()))
                z_services.append(np.log2(i.avg_outdegree_day()+1))
                

    fig = plt.figure(figsize = (10,10))
    ax = plt.axes(projection='3d')
    ax.grid()

    ax.scatter(x_crime, y_crime, z_crime, c = 'r') 
    ax.scatter(x_exchange, y_exchange, z_exchange, c = 'b')       
    ax.scatter(x_miner, y_miner, z_miner, c = 'y')       
    ax.scatter(x_services, y_services, z_services, c = 'g')       
          
    # plt.scatter(x_crime,y_crime,c = 'r')
    # plt.scatter(x_exchange,y_exchange,c = 'b')
    # plt.scatter(x_miner,y_miner,c = 'y')
    # plt.scatter(x_services,y_services,c = 'g')
    
    plt.show()