import os
import hashlib
import time

# Sending a message with encryption and signing
with open("names.txt", "r") as n:
    usernames = {line.strip().split(',')[0] for line in n}

sender = input("Enter the sender's username: ")
while sender not in usernames:
    sender = input("Enter a valid sender's username: ")

receiver = input("Enter the receiver's username: ")
while receiver not in usernames:
    receiver = input("Enter a valid receiver's username: ")

message = input("Enter the message to be sent: ")

# Encrypt the message with the recipient's public key
key_path = f"/PUBKEYS/{receiver}_pubK.pub"
encrypted_message_path = "encrypted_message.bin"
os.system(f"echo -n {message} | openssl rsautl -encrypt -pubin -inkey {key_path} -out {encrypted_message_path}")

# Calculate the SHA-256 hash of the encrypted message
with open(encrypted_message_path, "rb") as f:
    encrypted_message = f.read()
hash_object = hashlib.sha256(encrypted_message)

# Sign the hash object with the sender's private key
key_path = f"/home/{sender}/KEYS/{sender}_privK.pem"
signature_path = "signature.bin"
with open("hash.txt", "w") as hash_file:
    hash_file.write(hash_object.hexdigest())
os.system(f"openssl dgst -sha256 -sign {key_path} -out {signature_path} hash.txt")

# Send the signed and encrypted message to the receiver
message_path = "message.bin"
os.system(f"cat {signature_path} {encrypted_message_path} > {message_path}")
os.system(f"cp {message_path} /home/{receiver}/Messages/{message_path}")

# Print a confirmation message
print(f"Message sent from {sender} to {receiver}.")

# Receiving and verifying a message
receiver = input("Enter your username: ")
while receiver not in usernames:
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
with open("hash.txt", "w") as hash_file:
    hash_file.write(hash_object.hexdigest())
os.system(f"openssl dgst -sha256 -verify {key_path} -signature {signature_path} hash.txt")

# Decrypt the message with the receiver's private key
key_path = f"/home/{receiver}/KEYS/{receiver}_privK.pem"
decrypted_message_path = "decrypted_message.txt"
os.system(f"openssl rsautl -decrypt -inkey {key_path} -in {encrypted_message_path} -out {decrypted_message_path}")

# Read the decrypted message and calculate its hash
with open(decrypted_message_path, "r") as f:
    message = f.read()
hash_object = hashlib.sha256(message.encode())

# Compare the hash of the decrypted message with the hash of the encrypted message
if hash_object.hexdigest() == signature.decode().strip():
    print("Message received successfully and not tampered with.")
else:
    print("Error: Message tampered with.")
