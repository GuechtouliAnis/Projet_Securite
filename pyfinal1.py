import random
import string
import subprocess
import time
import cryptography
def generate_files (file_name,file_size):
    with open(file_name, 'w') as f:
        for i in range (file_size):
            f.write(random.choice(string.ascii_letters))
files={}
sizes = [10,20,50,100,200,500,1000]
encodes =["-aes-256-cbc","-aes-256-ecb","-des3-cbc","-des3-ecb"]
convert = 1024*1024
print(sizes)
sizelimit = input("enter size limit: ")
sizelimit = int(sizelimit)
while(sizelimit<0 or sizelimit>sizes[-1]):
    sizelimit = input("enter a valid size limit: ")
    sizelimit = int(sizelimit)
passwd = input("enter encryption password: ")
for i in sizes:
    if i <= sizelimit:
        st_cr = time.time()
        generate_files("random"+str(i)+"mb.txt", i*convert)
        e_t=time.time()-st_cr
        e_t1=e_t
        print("file "+str(i)+f" created with time of {e_t1: .5f} seconds")
        fileE = "random"+str(i)+"mb.txt"
        for j in encodes:
            fileO = str(i)+"mb"+str(j)+".cryp"
            start_time=time.time()
            command = f"openssl enc -e {j} -in {fileE} -out {fileO} -pass pass: {passwd}"
            end_time=time.time()-start_time
            e_time = end_time*1000
            print("file"+str(i)+str(j)+f" encrypted with time of {e_time: .10f} miliseconds")
            files1={"Size":str(i)+'mb',"Time":end_time}
            files[str(i)+'mb'+str(j)]=files1
