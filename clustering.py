import json
from analysis import user
import numpy as np
from sklearn.preprocessing import RobustScaler
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.cluster import KMeans

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
            
data = []

for i in user_list:
    i:user
    temp = []
    temp.append(np.log2(i.avg_indegree_day()+1))
    temp.append(np.log2(i.avg_out_transaction()+1))
    temp.append(np.log2(i.avg_outdegree_day()+1))
    temp.append(np.log2(i.avg_in_transaction()+1))
    temp.append(i.shortest_path)
    temp.append(i.frequency())
    data.append(temp)
    
colors = ['r','b','g','y']
color_idx = []
cmap = ListedColormap(colors)
data = np.array(data)    

transformer = RobustScaler().fit(data)
scaled_data = transformer.transform(data)
scaled_data = np.array(scaled_data)

U, s, VT = np.linalg.svd(scaled_data)
scaled_data = U[:,:6]*s[:6]

for i in user_list:
    color_idx.append(i.tag)

fig = plt.figure(figsize = (10,10),facecolor='white')
ax = plt.axes(projection='3d')
ax.grid(False)
ax.set_axis_off()
ax.scatter(scaled_data[:,0],scaled_data[:,1],scaled_data[:,2],c = color_idx,cmap=cmap)
plt.plot(scaled_data[:,0],scaled_data[:,1],scaled_data[:,2],color = 'pink')
plt.show()

number_clusters = 8
kmeans = KMeans(n_clusters=number_clusters, random_state=0, n_init="auto").fit(scaled_data)
centers = kmeans.cluster_centers_
labels = [[0,0,0,0] for i in range(number_clusters)]


for j in range(scaled_data.shape[0]):
    mini = -1
    mindis = np.inf
    for i in range(number_clusters):
        if mindis>np.linalg.norm(scaled_data[j]-centers[i]):
            mindis = np.linalg.norm(scaled_data[j]-centers[i])
            mini = i
    labels[mini][user_list[j].tag] += 1 
    
print(labels)
    
for i in range(number_clusters):
    maxi = max(labels[i])
    for j in range(4):
        if(maxi == labels[i][j]):
            labels[i] = j
            break
        
errors = 0

for j in range(scaled_data.shape[0]):
    mini = -1
    mindis = np.inf
    for i in range(number_clusters):
        if mindis>np.linalg.norm(scaled_data[j]-centers[i]):
            mindis = np.linalg.norm(scaled_data[j]-centers[i])
            mini = i
    if labels[mini]!=user_list[j].tag:
        errors+=1

print(len(user_list)) 
print(errors)
        
    
        
        
    





    







    


    