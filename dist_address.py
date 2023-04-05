import threading
import csv


lock = threading.Lock()
distinct = {}

def execute_fun(i):
    with open(f'data/{i}inp.csv','r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            lock.acquire()
            if(not (row[1] in distinct)):
                distinct[row[1]]= row[1]
            lock.release()
            print(len(distinct),end='\r')
            
    with open(f'data/{i}out.csv','r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            lock.acquire()
            if(not (row[1] in distinct)):
                distinct[row[1]]= row[1]
            lock.release()
            print(len(distinct),end='\r')
            
        
        
if __name__ == '__main__':
    
    threads = []
    for i in range(30):
        t = threading.Thread(group=None, target=execute_fun, name=None, args=(i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("process1 completed")
    with open('distinct.csv',mode = 'a',newline='') as file:
        wrrittter = csv.writer(file)
        
        for i in distinct:
            wrrittter.writerow([i,i])
    print("process 2 completed")