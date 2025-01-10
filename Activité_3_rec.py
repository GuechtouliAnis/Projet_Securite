import os
import hashlib
import time

# Check if the script is running with root privileges
if os.geteuid() == 0:
    # Create the /PUBKEYS directory
    os.system('mkdir /PUBKEYS')

    # Open the 'names.txt' file in read mode
    with open('names.txt', 'r') as f:
        # Loop through each line in the file
        for line in f:
            # Split the line into username and password based on the comma separator
            username, password = line.strip().split(',')

            # Create a new user with the specified username and password
            print(f"Creating user {username} with password {password}...")
            os.system(f'useradd -m {username}')
            os.system(f'echo {username}:{password} | chpasswd')
            print(f"User {username} created.")

            # Create a KEYS directory in the user's home directory
            os.system(f'mkdir -p /home/{username}/KEYS')
            os.system(f'chown {username}:{username} /home/{username}/KEYS')

            # Generate a private key for the user
            print(f"Generating private key for {username}...")
            os.system(f'openssl genrsa -out /home/{username}/KEYS/{username}_privK.pem 2048')

            # Generate a public key from the private key
            print(f"Generating public key for {username}...")
            os.system(f'openssl rsa -in /home/{username}/KEYS/{username}_privK.pem -out /home/{username}/KEYS/{username}_pubK.pub -pubout')
            os.system(f'cp /home/{username}/KEYS/{username}_pubK.pub /PUBKEYS/{username}_pubK.pub')

            # Adjust permissions for the user's keys
            print(f"Adjusting permissions for {username}'s keys...")
            os.system(f'chmod 600 /home/{username}/KEYS')
            os.system(f'chmod 400 /home/{username}/KEYS/{username}_privK.pem')
            os.system(f'chmod 644 /home/{username}/KEYS/{username}_pubK.pub')
            os.system(f'chmod 644 /PUBKEYS/{username}_pubK.pub')

            # Change ownership of the key files to the user
            os.system(f'chown {username}:{username} /home/{username}/KEYS/{username}_privK.pem')
            os.system(f'chown {username}:{username} /home/{username}/KEYS/{username}_pubK.pub')
            os.system(f'chown {username}:{username} /PUBKEYS/{username}_pubK.pub')

            # Print completion message for the user
            print(f"Private and public keys generated for {username}.")

else:
    # Print an error message if the script is not run as root
    print("Current user is not root, please login as root and try again")

# Receiving and verifying a message
with open("names.txt", "r") as n:
    for i in n:
        username, password = i.strip().split(',')
receiver = input("Enter your username: ")

# Check if the receiver's username exists
if receiver not in username:
    exists = 0
else:
    exists = 1

while not exists:
    receiver = input("Enter a valid username: ")

message_path = f"/home/{receiver}/Messages/message.bin"

# Wait for the message to be received
while not os.path.isfile(message_path):
    time.sleep(5)

# Read the received message and extract the signature and encrypted message
with open(message_path, "rb") as f:
    signature = f.read(256)
    encrypted_message = f.read()

# Verify the signature with the sender's public key
sender_username = message_path.split("/")[-2]
key_path = f"/PUBKEYS/{sender_username}_pubK.pub"
hash_object = hashlib.sha256(encrypted_message)
os.system(f"openssl dgst -sha256 -verify {key_path} -signature <(echo -n '{signature.decode()}') <(echo -n '{hash_object.hexdigest()}')")

# Decrypt the message with the receiver's private key
key_path = f"/home/{receiver}/KEYS/{receiver}_privK.pem"
decrypted_message_path = "decrypted_message.txt"
os.system(f"openssl rsautl -decrypt -inkey {key_path} -in {encrypted_message} -out {decrypted_message_path}")

# Read the decrypted message and calculate its hash
with open(decrypted_message_path, "r") as f:
    message = f.read()
hash_object = hashlib.sha256(message.encode())

# Compare the hash of the decrypted message with the hash of the encrypted message
if hash_object.hexdigest() == signature.decode().strip():
    print("Message received successfully and not tampered with.")
else:
    print("Error: Message tampered with.")
