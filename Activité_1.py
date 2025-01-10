import random
import string
import time
import matplotlib.pyplot as plt

# Function to generate random text files of specified size in MB
def generate_files(file_name, file_size):
    with open(file_name, 'w') as f:
        for i in range(file_size):
            f.write(random.choice(string.ascii_letters))

# Dictionaries to store encryption times for AES and DES
AES = {}
DES = {}

# Different file sizes to test (in MB)
sizes = [10, 20, 50, 100, 200, 500, 1000, 2000]

# Encryption algorithms to test for AES and DES
encryption_aes = ["-aes-256-cbc", "-aes-256-ecb"]
encryption_des = ["-des3-cbc", "-des3-ecb"]

# Conversion factor to convert size from MB to bytes
convert_size = 1024 * 1024

# Prompt the user for size limit and encryption password
sizelimit = input("Enter a size limit: ")
sizelimit = int(sizelimit)
while sizelimit < 0 or sizelimit > sizes[-1]:
    sizelimit = input("Enter a valid size limit: ")
    sizelimit = int(sizelimit)
passwd = input("Enter encryption password: ")

# Iterate through file sizes up to the specified limit
for i in sizes:
    if i <= sizelimit:
        print(f"Generating file of {i} MB")
        generate_files(f"random{i}mb.txt", i * convert_size)
        print("File generated successfully")
        fileIn = f"random{i}mb.txt"

        # AES encryption
        for j in encryption_aes:
            fileOut = f"{i}mb{j}.cryp"
            start_time = time.time()
            command = f"openssl enc -e {j} -in {fileIn} -out {fileOut} -pass pass:{passwd}"
            # Note: The command execution is missing here; it needs os.system(command) to actually run
            end_time = time.time() - start_time
            end_time = end_time * 1000
            print(f"File {i} MB encrypted with {j} in {end_time:.10f} milliseconds")
            AES[f"{i}mb_{j[-3:]}"] = {"Type": j[-3:], "Size": f"{i}mb", "Time": end_time}

        # DES encryption
        for k in encryption_des:
            fileOut = f"{i}mb{k}.cryp"
            start_time = time.time()
            command = f"openssl enc -e {k} -in {fileIn} -out {fileOut} -pass pass:{passwd}"
            # Note: The command execution is missing here; it needs os.system(command) to actually run
            end_time = time.time() - start_time
            end_time = end_time * 1000
            print(f"File {i} MB encrypted with {k} in {end_time:.10f} milliseconds")
            DES[f"{i}mb_{k[-3:]}"] = {"Type": k[-3:], "Size": f"{i}mb", "Time": end_time}

# Convert AES and DES data to lists for plotting
AES_data = list(AES.values())
DES_data = list(DES.values())

# Plotting the encryption times
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# Plot AES encryption times for CBC and ECB modes
for data_type in ['cbc', 'ecb']:
    data = [d for d in AES_data if d['Type'] == data_type]
    axs[0].plot([d['Size'] for d in data], [d['Time'] for d in data], marker='o', label=data_type)
axs[0].set_xlabel('Size')
axs[0].set_ylabel('Time (ms)')
axs[0].set_title('AES Encryption Times')
axs[0].legend()

# Plot DES encryption times for CBC and ECB modes
for data_type in ['cbc', 'ecb']:
    data = [d for d in DES_data if d['Type'] == data_type]
    axs[1].plot([d['Size'] for d in data], [d['Time'] for d in data], marker='s', label=data_type)
axs[1].set_xlabel('Size')
axs[1].set_ylabel('Time (ms)')
axs[1].set_title('DES Encryption Times')
axs[1].legend()

# Display the plots
plt.show()