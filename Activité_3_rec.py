import os
import hashlib
import time

with open("names.txt", "r") as n:
    for i in n:
        username, password = i.strip().split(',')
receiver = input("Enter your username: ")

if receiver not in username:
    exists = 0
else:
    exists = 1
while(not exists):
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
