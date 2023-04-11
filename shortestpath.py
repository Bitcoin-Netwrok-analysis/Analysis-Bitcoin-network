from analysis import user
import json

final_users = []

with open('second_last.json', 'r') as f:
    for line in f:
        user_dict = json.loads(line)
        User = user(user_dict['user_id'], user_dict['out_id'], user_dict['in_id'], user_dict['in_degree_days'],user_dict['out_degree_days'],user_dict['shortest_path'])
        final_users.append(User)
        

print('process 1 completed')
bfs = []
for i in final_users:
    if i.shortest_path==0:
        bfs.append(i)

def BFS(bfs):
    temp = []
    
    if len(bfs)==0:
        return
    num = bfs[0].shortest_path+1
    print(num)
    for i in bfs:
        for j in i.in_id:
            if final_users[int(j)].shortest_path != None:
                final_users[int(j)].shortest_path = num
                temp.append(final_users[int(j)])
    del bfs
    BFS(temp) 
    
BFS(bfs)
print('process 2 completed')

with open('last.json', 'w') as f:
    for i in (final_users):
        i_dict = i.to_dict()
        json.dump(i_dict, f)
        f.write('\n') 
print('process 3 completed')