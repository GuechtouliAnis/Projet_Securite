import string
import random
import subprocess
import time
import cryptography
import matplotlib.pyplot as plt
files = {}
sizes = [1,2,3,4]
#Create random files with multiple sizes
def generate_part1 (file_name,file_size):
    with open(file_name, 'w') as f:
        for i in range (file_size):
            f.write(random.choice(string.ascii_letters))
default=1024*1024
j = 1
for i in sizes:
    start_time = time.time()
    generate_part1('random'+str(i)+'mb.txt', i*default)
    end_time=time.time()-start_time
    files1={"Size":str(i)+'mb',"Time":end_time}
    files["child"+str(j)] =files1
    print("child "+str(j)+" encoded succesfully with a creation time of "+str(end_time))
    j+=1
x_values = [child_dict["Size"] for child_dict in files.values()]
y_values = [child_dict["Time"] for child_dict in files.values()]
plt.plot(x_values, y_values, marker='o')
plt.xlabel("Size")
plt.ylabel("Time")
plt.title("File Creation Time by Size")
plt.show()
# Run the `ls` command and print its output
#output = subprocess.run(['ls', '-al'], capture_output=True, text=True)
#print(output.stdout)