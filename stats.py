import csv

addresses = []
with open('tag.csv', mode ='r')as file:
   
  # reading the CSV file
  csvFile = csv.reader(file)
 
  # displaying the contents of the CSV file
  for lines in csvFile:
        if(len(lines)==0):
            continue
        addresses.append(lines[0])
        
def binary_search(s,e,key,addresses):
    if s==e and addresses[s]==key:
        return s
    elif s==e:
        return -1
        
    mid = (s+e)//2
    if(addresses[mid]<key):
        return binary_search(mid+1,e,key,addresses)
    else:
        return binary_search(s,mid,key,addresses)

addresses.sort()
check = [False for i in range(len(addresses))]
ans = 0
for i in range(30):
    with open(f'data/{i}inp.csv',mode = 'r') as file:
        csvFile = csv.reader(file)
        
        for lines in csvFile:
            ind = binary_search(0, len(addresses)-1, lines[1],addresses)
            if ind!=-1:
                if not check[ind]:
                    ans+=1
                    check[ind] = True
    print(ans)

print(ans)
            

    


        
