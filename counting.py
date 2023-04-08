import csv 
import matplotlib.pyplot as plt

count = [0 for i in range(7835865)]
with open('cluster.csv', 'r') as file:
    reader = csv.reader(file)
    
    for row in reader:
        count[int(row[1])]+=1

y = [0 for i in range(50)]
for i in count:
    if i>=49:
        y[49]+=1
    else:
        y[i]+=1

x = [i+1 for i in range(50)]

plt.bar(x,y)
plt.show()