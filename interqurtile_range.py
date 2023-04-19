import numpy as np
from sklearn.preprocessing import RobustScaler
import csv

mu, sigma = 100, 50 # mean and standard deviation
num_samples = 10000
# Generate random data from a Gaussian distribution
gaussian_data = np.random.normal(100, sigma, num_samples)

gaussian_data2 = np.random.normal(800.1,200,10000)

data2 = np.concatenate((gaussian_data,gaussian_data2))

data = [0 for i in range(1000)]

for i in data2:
        if i>=999: data[999]+=1
        elif i<=0: data[0]+=1
        else: data[int(i)]+=1

    


scaler = RobustScaler()
scaled_data2 =   scaler.fit_transform(data2.reshape((-1,1)))
scaled_data2 = scaled_data2.flatten()
scaled_data2 = np.sort(scaled_data2)
num = scaled_data2[0]
scaled_data = [0 for i in range(1000)]
for i in scaled_data2:
    j = i+3
    if j*100>=1000: scaled_data[999]+=1
    elif j*100<=0: scaled_data[0]+=1
    else: scaled_data[int(j*100)]+=1
data = np.delete(data,-1)
scaled_data = np.delete(scaled_data,-1)

with open('graph/scaling.csv',mode = 'w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(data)
    writer.writerow(scaled_data)
    




