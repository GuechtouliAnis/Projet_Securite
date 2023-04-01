import os
import hashlib

with open("names.txt", "r") as n:
    for i in n:
        username, password = i.strip().split(',')
sender = input("Enter the sender's username: ")
receiver = input("Enter the receiver's username: ")

if sender not in username:
    exists = 0
else:
    exists = 1
while(not exists):
    sender = input("Enter a valid sender's username: ")
if receiver not in username:
    exists = 0
else:
    exists = 1
while(not exists):
    receiver = input("Enter a valid receiver's username: ")
message = input("Enter the message to be sent: ")

# Encrypt the message with the recipient's public key
key_path = f"/PUBKEYS/{receiver}_pubK.pub"
encrypted_message_path = "encrypted_message.bin"
os.system(f"openssl rsautl -encrypt -pubin -inkey {key_path} -in <(echo -n {message}) -out {encrypted_message_path}")

# Calculate the SHA-256 hash of the encrypted message
with open(encrypted_message_path, "rb") as f:
    encrypted_message = f.read()
hash_object = hashlib.sha256(encrypted_message)

# Sign the hash object with the sender's private key
key_path = f"/home/{sender}/KEYS/{sender}_privK.pem"
signature_path = "signature.bin"
os.system(f"openssl dgst -sha256 -sign {key_path} -out {signature_path} {hash_object.hexdigest()}")

# Send the signed and encrypted message to the receiver
message_path = "message.bin"
os.system(f"cat {signature_path} {encrypted_message_path} > {message_path}")
os.system(f"cp {message_path} /home/{receiver}/Messages/{message_path}")

# Print a confirmation message
print(f"Message sent from {sender} to {receiver}.")
