import threading
import mysql.connector
from disjointset import DisjSet
import csv


# Create a connection pool
conn_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=32,
    host="localhost",
    user="root",
    password="Mihir@2811",
    database="bitcoindatabase"
)
lock = threading.Lock()


# Define a function that will be executed by each thread
def execute_query(thread_id):
    # Get a connection from the pool
    conn = conn_pool.get_connection()

    # Execute a query
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM trans_detail WHERE day = {thread_id}")
    result = cursor.fetchall()
    for i in result:
        cursor.execute(f"SELECT address from inputs where id={i[0]}")
        resul = cursor.fetchall()
        if len(resul)>0:
            lock.acquire()
            fad = resul[0][0]
            for j in range(1,len(resul)):
                ds.Union(fad,resul[j][0])
            lock.release()
        print(i[0],end = '\r')
                
       
    # Release the connection back to the pool
    conn.close()

# Create 5 threads and start them
if __name__=='__main__':
    parent = {}
    
    with open('distinct.csv','r') as file:
        reader = csv.reader(file)
        
        for i in reader:
            parent[i[0]] = i[0]
            
    global ds
    ds = DisjSet(parent)
    threads =[]
    for i in range(0,30):
        t = threading.Thread(target=execute_query, args=(i,))
        threads.append(t)
        t.start()
    for i in threads:
        i.join()
    id_dict={}
    count = 0
    for i in ds.parent:
        ds.find(i)
    for i in ds.parent:
        if(ds.parent[i] in id_dict):
            ds.parent[i]=id_dict[ds.parent[i]]
        else:
            id_dict[ds.parent[i]]=count
            ds.parent[i]=count
            count+=1
    with open('cluster.csv',mode = 'a', newline='') as file:
        writer1 = csv.writer(file)
        
        for i in ds.parent:
            writer1.writerow([i,ds.parent[i]])
             
         
    
        
    