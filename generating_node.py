import threading
import mysql.connector
from disjointset import DisjSet
import csv
import json

class user:
    
    def __init__(self, user_id, lock):
        self.lock = lock
        self.user_id = user_id
        self.out_id = {}
        self.in_id = {}
        self.in_degree_days = {}
        self.out_degree_days = {}
        self.shortest_path = None
    def to_dict(self):
        return {'user_id': self.user_id,
                'out_id': self.out_id,
                'in_id': self.in_id,
                'in_degree_days': self.in_degree_days,
                'out_degree_days': self.out_degree_days,
                'shortest_path': self.shortest_path }

add_to_id = {}
with open('cluster.csv', mode = 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        add_to_id[row[0]] = int(row[1])

users = []
locks = []
for i in range(31):
    locks.append(threading.Lock())
for i in range(7835865):
    users.append(user(i,locks[i//261195]))
    
conn_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=32,
    host="localhost",
    user="root",
    password="Mihir@2811",
    database="bitcoindatabase"
)

def execution_fun(day):
    NUM = 100000000
    conn = conn_pool.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id from trans_detail where day={day}")
    ids = cursor.fetchall()
    for id in ids:
        cursor.execute(f"SELECT id from coinjoin where id={id[0]}")
        is_join = cursor.fetchall()
        is_join = (len(is_join)!=0)
        cursor.execute(f"SELECT address,value from inputs where id ={id[0]}")
        inputs = cursor.fetchall()
        cursor.execute(f"SELECT address,value from outputs where id ={id[0]}")
        outputs = cursor.fetchall()
        user_id = 0
        if len(inputs)>0:
            user_id = add_to_id[inputs[0][0]]
        else:
            continue
        outusers = {}
        for i in outputs:
            out_user_id = add_to_id[i[0]]
            if(out_user_id in outusers):
                outusers[out_user_id]+=(i[1]/NUM)
            else:
                outusers[out_user_id]=(i[1]/NUM)
                
        users[user_id].lock.acquire()
        if is_join:
            users[user_id].shortest_path = 0
        for out_user_id in outusers:
            if(out_user_id==user_id):
                continue
            if(out_user_id in users[user_id].out_id):
                users[user_id].out_id[out_user_id]+=(outusers[out_user_id])
            else:
                users[user_id].out_id[out_user_id]=(outusers[out_user_id])
            if(day in users[user_id].out_degree_days):
                users[user_id].out_degree_days[day]+=1
            else:
                users[user_id].out_degree_days[day]=1
                
        users[user_id].lock.release()
        
        for i in outusers:
            if(i==user_id):
                continue
            users[i].lock.acquire()
            if(user_id in users[i].in_id):
                users[i].in_id[user_id]+=outusers[i]
            else:
                users[i].in_id[user_id]=outusers[i]
            if(day in users[i].in_degree_days):
                users[i].in_degree_days[day]+=1
            else:
                users[i].in_degree_days[day]=1
            users[i].lock.release()
        print(id[0],end='\r')
            
if __name__ =='__main__':
    threads = []
    for i in range(30):
        t = threading.Thread(target=execution_fun,args=(i,) )
        threads.append(t)
        t.start()
    
    for i in threads:
        i.join()
    
    with open('second_last.json', 'w') as f:
        for i in (users):
            i_dict = i.to_dict()
            json.dump(i_dict, f)
            f.write('\n') 