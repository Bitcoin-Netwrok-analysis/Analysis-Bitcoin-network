import json
from analysis import user
import csv
import numpy as np
user_list = []
counter = 0
with open('final.json','r') as f:
    for line in f:
        user_dict = json.loads(line)
        if user_dict['tag']==1:
            counter+=1
            if counter>30:
                continue
            else:
                user_list.append(user(user_dict['user_id'],user_dict['out_id'],user_dict['in_id'],user_dict['in_degree_days'],user_dict['out_degree_days'], user_dict['shortest_path'],user_dict['tag']))            
        else:
            user_list.append(user(user_dict['user_id'],user_dict['out_id'],user_dict['in_id'],user_dict['in_degree_days'],user_dict['out_degree_days'], user_dict['shortest_path'],user_dict['tag']))
            
x = [i for i in range(20)]
crime = ['crime']
exchange = ['exchange']
miner = ['miner']
service = ['service']

for i in user_list:
    i:user
    value = i.shortest_path
    if i.tag==0 and len(crime)<21:
        crime.append(value)
    elif i.tag==1 and len(exchange)<21:
        exchange.append(value)
    elif i.tag==2 and len(miner)<21:
        miner.append(value)
    elif i.tag==3 and len(service)<21:
        service.append(value)
        
# for i in range(2,len(crime)):
#     crime[i] = crime[i]+crime[i-1]
    
# for i in range(2,len(exchange)):
#     exchange[i] = exchange[i]+exchange[i-1]
    
# for i in range(2,len(miner)):
#     miner[i] = miner[i]+miner[i-1]
    
# for i in range(2,len(service)):
#     service[i] = service[i]+service[i-1]
    
# for i in range(2,len(crime)):
#     crime[i] = crime[i]/i
    
# for i in range(2,len(exchange)):
#     exchange[i] = exchange[i]/i
    
# for i in range(2,len(miner)):
#     miner[i] = miner[i]/i

# for i in range(2,len(service)):
#     service[i] = service[i]/i
        

        
with open('graph/path.csv', mode= 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(crime)
    writer.writerow(exchange)
    writer.writerow(miner)
    writer.writerow(service)
    
    

