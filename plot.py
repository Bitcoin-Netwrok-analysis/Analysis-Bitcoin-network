from matplotlib import pyplot as plt    
from matplotlib import pyplot as plt 
import csv

counter = []

with open('input1.csv', mode ='r')as file:
   
  # reading the CSV file
  csvFile = csv.reader(file)

  # displaying the contents of the CSV file
  for line in csvFile:
      if len(line)==0:
          continue
      num = int(line[0])
      
      while len(counter)<=num:
          counter.append(0)
      else:
          counter[-1]+=1
      
count = 0
for i in counter:
    if( i > 50):
        count+=1
print(count)  

   
trans_index = [i for i in range(0,len(counter))]      
plt.plot(trans_index, counter)    
plt.xlabel('index')    
plt.ylabel('input transaction')    
plt.title('# inputs')    
plt.show()  


