import random
import string
import subprocess
import time
import matplotlib.pyplot as plt

def generate_files (file_name,file_size):
    with open(file_name, 'w') as f:
        for i in range (file_size):
            f.write(random.choice(string.ascii_letters))

AES={}
DES={}
sizes = [10,20,50,100,200,500,1000,2000]
encryption_aes=["-aes-256-cbc","-aes-256-ecb"]
encryption_des=["-des3-cbc","-des3-ecb"]
convert_size = 1024*1024

sizelimit = input("Enter a size limit: ")
sizelimit = int(sizelimit)
while(sizelimit<0 or sizelimit>sizes[-1]):
    sizelimit = input("enter a valid size limit: ")
    sizelimit = int(sizelimit)
passwd = input("enter encryption password: ")

for i in sizes:
    if i<= sizelimit:
        print("Generating file of "+str(i)+"mb")
        generate_files("random"+str(i)+"mb.txt",i*convert_size)
        print("File generated successfully")
        fileIn = "random"+str(i)+"mb.txt"
        for j in encryption_aes:
            fileOut = str(i)+"mb"+str(j)+".cryp"
            start_time = time.time()
            command = f"openssl enc -e {j} -in {fileIn} -out {fileOut} -pass pass: {passwd}"
            end_time = time.time()-start_time
            end_time = end_time*1000
            print("file"+str(i)+"mb"+str(j)+f"encrypted with a time of {end_time: .10} miliseconds")
            AES_T={"Type":j[-3:],"Size":str(i)+'mb',"Time":end_time}
            AES[str(i)+'mb_'+str(j[-3:])]=AES_T
        for k in encryption_des:
            fileOut = str(i)+"mb"+str(k)+".cryp"
            start_time = time.time()
            command = f"openssl enc -e {k} -in {fileIn} -out {fileOut} -pass pass: {passwd}"
            end_time = time.time()-start_time
            end_time = end_time*1000
            print("file"+str(i)+"mb"+str(k)+f"encrypted with a time of {end_time: .10} miliseconds")
            DES_T={"Type":k[-3:],"Size":str(i)+'mb',"Time":end_time}
            DES[str(i)+'mb_'+str(k[-3:])]=AES_T

AES_data = list(AES.values())
DES_data = list(DES.values())

fig, axs = plt.subplots(1, 2, figsize=(10, 5))

for data_type in ['cbc', 'ecb']:
    data = [d for d in AES_data if d['Type'] == data_type]
    axs[0].plot([d['Size'] for d in data], [d['Time'] for d in data], marker='o', label=data_type)
axs[0].set_xlabel('Size')
axs[0].set_ylabel('Time')
axs[0].set_title('AES')
axs[0].legend()

for data_type in ['cbc', 'ecb']:
    data = [d for d in DES_data if d['Type'] == data_type]
    axs[1].plot([d['Size'] for d in data], [d['Time'] for d in data], marker='s', label=data_type)
axs[1].set_xlabel('Size')
axs[1].set_ylabel('Time')
axs[1].set_title('DES')
axs[1].legend()

plt.show()
