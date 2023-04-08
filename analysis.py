from enum import Enum
import csv
import json
import matplotlib.pyplot as plt
import numpy as np

class Tag(Enum):
    CRIMINAL = 0
    EXCHANGE = 1
    SERVICES = 2
    MINER =3
    UNTAGGED = 4
    

class user:
    
    def __init__(self, user_id, out_id,in_id, in_degree_days, out_degree_days,shortest_path = None,lock =None):
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
    with open('second_last.json', 'r') as f:
        counter = 0
        for line in f:
            user_dict = json.loads(line)
            if counter in users:
                User = user(user_dict['user_id'], user_dict['out_id'], user_dict['in_id'], user_dict['in_degree_days'],user_dict['out_degree_days'])
                User.tag = users[counter]
                final_users.append(User)
            counter+=1
    del users
    print('process 3 completed')
    
    
    x = []
    y = []
    for i in final_users:
        match i.tag:
            case Tag.CRIMINAL:
                x.append(2)
            case Tag.EXCHANGE:
                x.append(1)
            case Tag.MINER:
                x.append(3)
            case Tag.SERVICES:
                x.append(4)
        y.append(3*np.log(i.frequency()+1))
    plt.scatter(x,y)
    plt.show()
    
    
    
            
    

            
    
    
    
        
        
            
        
    
    