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
        count = result[0][0]
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
    
def check_coinjoin(inputs, outputs):
    NUM = 100000000
    def scdh():
        check = False
        if len(inputs)==5 and len(outputs)==5:
            check = True
            p = outputs[0][3]
            for i in outputs:
                if i[3]!=p:
                    check=False
                    break
            count = 0
            for i in inputs:
                if i[3]==p:
                    count+=1
            if count==0 or count>=4:
                check=False
        return check
    
    def wcdh():
        output_counts = {}
        if len(outputs)==0:
            return False
        for output in outputs:
            if output[3] in output_counts:
                output_counts[output[3]] += 1
            else:
                output_counts[output[3]] = 1
        
        # Check if there are at least ten equal value outputs
        most_frequent_output = max(output_counts, key=output_counts.get)
        if output_counts[most_frequent_output] < 10:
            return False
        
        # Check if the most frequent output is 0.1 ± 0.02 BTC
        if abs(most_frequent_output/NUM - 0.1) > 0.02:
            return False
        
        # Count the number of distinct output values
        num_distinct_outputs = len(output_counts)
        
        # Check if there are at least three distinct output values
        if num_distinct_outputs < 3:
            return False
        
        # Check if there is at least one unique output value
        most_least = min(output_counts, key=output_counts.get)
        if output_counts[most_least] > 1:
            return False
        
        # Check if the transaction has at least as many inputs as occurrences of the most frequent output
        if len(inputs) < output_counts[most_frequent_output]:
            return False
        
        # If all checks pass, the transaction is a Wasabi Wallet CoinJoin transaction
        print('FUCK')
        return True
    return scdh() or wcdh()
         
            
            
            
    
    
    
def finding_coin_join():
    dataBase = mysql.connector.connect(user = 'root',
                               host = 'localhost',
                              password = 'Mihir@2811')
    cursorObject = dataBase.cursor() 
    cursorObject.execute("USE BitcoinDatabase")
    cursorObject.execute("DROP TABLE IF EXISTS coinjoin")
    cursorObject.execute("""CREATE TABLE coinjoin(id INT PRIMARY KEY,
                                                  FOREIGN KEY (id) REFERENCES trans_detail(id))""")
    dataBase.commit()
    # cursorObject.execute("DROP index idx_i on inputs")
    # cursorObject.execute("DROP index idx_o on outputs")
    # cursorObject.execute("DROP index idx_c on coinjoin")
    dataBase.commit()
    # cursorObject.execute("CREATE INDEX idx_i ON inputs(id) USING HASH;")
    # cursorObject.execute("CREATE INDEX idx_o ON outputs(id) USING HASH;")
    cursorObject.execute("CREATE INDEX idx_c ON coinjoin(id) USING HASH;")
    dataBase.commit()
    
    for i in range(1,7693857):
        cursorObject.execute(f"SELECT * from inputs where id={i}")
        inputs = cursorObject.fetchall()
        cursorObject.execute(f"SELECT * from outputs where id={i}")
        outputs = cursorObject.fetchall()
        if check_coinjoin(inputs,outputs):
            cursorObject.execute(f"INSERT INTO coinjoin (id) VALUES ({i})")
            dataBase.commit()
    dataBase.close()
    
def distinct_addresses():
    dataBase = mysql.connector.connect(user = 'root',
                               host = 'localhost',
                              password = 'Mihir@2811')
    cursorObject = dataBase.cursor() 
    cursorObject.execute("USE BitcoinDatabase")
    cursorObject.execute("DROP TABLE IF EXISTS user")
    cursorObject.execute("""CREATE TABLE user(address VARCHAR(255) PRIMARY KEY,
                                                  user_id INT)""")
    dataBase.commit()
    cursorObject.execute("CREATE INDEX idx_ua ON user(address) USING HASH;")
    dataBase.commit()
    cursorObject.execute("CREATE INDEX idx_ui ON user(user_id) USING HASH;")
    dataBase.commit()
    for i in range(1,7693857):
        cursorObject.execute(f"SELECT * from inputs where id={i}")
        inputs = cursorObject.fetchall()
        cursorObject.execute(f"SELECT * from outputs where id={i}")
        outputs = cursorObject.fetchall()
        for j in inputs:
            add = j[1]
            cursorObject.execute(f"SELECT * from user where address='{add}'")
            result = cursorObject.fetchall()
            if len(result)==0:
                cursorObject.execute(f"INSERT INTO user (address,user_id) VALUES ('{add}',-1)")
                dataBase.commit()
        for j in outputs:
            add = j[1]
            cursorObject.execute(f"SELECT * from user where address='{add}'")
            result = cursorObject.fetchall()
            if len(result)==0:
                cursorObject.execute(f"INSERT INTO user (address,user_id) VALUES ('{add}',-1)")
                dataBase.commit()
            
        
    
    
    
    
    

    
if __name__=='__main__':
    finding_coin_join()
                
    # Disconnecting from the server
    