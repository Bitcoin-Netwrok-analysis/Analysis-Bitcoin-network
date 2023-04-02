import os

folder = "data"
count = 0
filenames = os.listdir(folder)
filenames.sort()
for filename in filenames:
    dst = f"{str(count)}out.csv"
    src =f"{folder}/{filename}"  # foldername/filename, if .py file is outside folder
    dst =f"{folder}/{dst}"
        
    # rename() function will
    # rename all the files
    if filename[-5]=='t':
        os.rename(src, dst)
        count+=1
    