import mysql.connector
import csv
from multiprocessing import Pool
 



def set_data(i):
    dataBase = mysql.connector.connect(user = 'root',
                               host = 'localhost',
                              password = 'Mihir@2811')
    cursorObject = dataBase.cursor() 
    cursorObject.execute("USE BitcoinDatabase")
    
    print('processing')
    inputs = []
    outputs = []
    with open(f'data/{i}inp.csv', 'r') as file:

        # Create a CSV reader object
        reader = csv.reader(file)

        # Loop over each row in the CSV file
        for row in reader:
            inputs.append(row)
    with open(f'data/{i}out.csv', 'r') as file:

        # Create a CSV reader object
        reader = csv.reader(file)

        # Loop over each row in the CSV file
        for row in reader:
            outputs.append(row)
    prev = -1
    for j in inputs:
        if int(j[0])!=prev:
            cursorObject.execute(f"SELECT * from trans_detail where day={i} and indx={j[0]}")
            result = cursorObject.fetchall()
        else:
            prev = int(j[0])
        if(len(result)==0):
            cursorObject.execute(f"INSERT INTO trans_detail (day, indx) VALUES ({i},{j[0]})")
            dataBase.commit()
            cursorObject.execute(f"SELECT * from trans_detail where day={i} and indx={j[0]}")
            result = cursorObject.fetchall()
            
        count = result[0][0]
        
        address = j[1]
        cursorObject.execute(f"INSERT INTO inputs (address, id, value) VALUES ('{address}',{count},{j[2]})")
        dataBase.commit()
    prev = -1
    for j in outputs:
        if int(j[0])!=prev:
            cursorObject.execute(f"SELECT * from trans_detail where day={i} and indx={j[0]}")
            result = cursorObject.fetchall()
        else:
            prev= int(j[0])
        
        if(len(result)==0):
            cursorObject.execute(f"INSERT INTO trans_detail (day, indx) VALUES ({i},{j[0]})")
            dataBase.commit()
            cursorObject.execute(f"SELECT * from trans_detail where day={i} and indx={j[0]}")
            result = cursorObject.fetchall()
        count = cursorObject.fetchall()[0][0]
        
        
        address = j[1]
        cursorObject.execute(f"INSERT INTO outputs (address, id, value) VALUES ('{address}',{count},{j[2]})")
        dataBase.commit()
        
    dataBase.commit()
    dataBase.close()


def set_up_database():
    dataBase = mysql.connector.connect(user = 'root',
                               host = 'localhost',
                              password = 'Mihir@2811')
    cursorObject = dataBase.cursor() 
    cursorObject.execute("DROP Database IF EXISTS BitcoinDatabase")    
    dataBase.commit()
    cursorObject.execute("CREATE DATABASE BitcoinDatabase")
    dataBase.commit()
    cursorObject.execute("USE BitcoinDatabase")
    dataBase.commit()
    
    cursorObject.execute("""CREATE TABLE trans_detail(id INT PRIMARY KEY AUTO_INCREMENT,
                                                      day INT,
                                                      indx INT)""")
    dataBase.commit()
    cursorObject.execute("""CREATE TABLE inputs(id_ INT PRIMARY KEY AUTO_INCREMENT,
                                                address VARCHAR(255),
                                                id INT,
                                                value BIGINT,
                                                FOREIGN KEY (id) REFERENCES trans_detail(id))""")
    dataBase.commit()
    cursorObject.execute("""CREATE TABLE outputs(id_ INT PRIMARY KEY AUTO_INCREMENT,
                                                address VARCHAR(255),
                                                id INT,
                                                value BIGINT,
                                                FOREIGN KEY (id) REFERENCES trans_detail(id))""")
    dataBase.commit()
    cursorObject.execute("CREATE INDEX idx_ ON trans_detail(day,indx) USING HASH;")
    dataBase.commit()
    with Pool(30) as p:
        p.map(set_data,[i for i in range(0,30)])
        
    dataBase.close()
    

    
if __name__=='__main__':
            
    pass
                
    # Disconnecting from the server
    