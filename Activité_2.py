#!/usr/bin/env python
import os

if os.geteuid() == 0:
    os.system('mkdir /PUBKEYS')
    with open('names.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split(',')

            print(f"Creating user {username} with password {password}...")
            os.system(f'useradd -m {username}')
            os.system(f'echo {username}:{password} | chpasswd')
            print(f"User {username} created.")

            os.system(f'mkdir -p /home/{username}/KEYS')
            os.system(f'chown {username}:{username} /home/{username}/KEYS')

            print(f"Generating private key for {username}...")
            os.system(f'openssl genrsa -out /home/{username}/KEYS/{username}_privK.pem 2048')

            print(f"Generating public key for {username}...")
            os.system(f'openssl rsa -in /home/{username}/KEYS/{username}_privK.pem -out /home/{username}/KEYS/{username}_pubK.pub -pubout')
            os.system(f'cp /home/{username}/KEYS/{username}_pubK.pub /PUBKEYS/{username}_pubK.pub')

            print(f"Adjusting permissions for {username}'s keys...")
            os.system(f'chmod 600 /home/{username}/KEYS')
            os.system(f'chmod 400 /home/{username}/KEYS/{username}_privK.pem')
            os.system(f'chmod 644 /home/{username}/KEYS/{username}_pubK.pub')
            os.system(f'chmod 644 /PUBKEYS/{username}_pubK.pub')

            os.system(f'chown {username}:{username} /home/{username}/KEYS/{username}_privK.pem')
            os.system(f'chown {username}:{username} /home/{username}/KEYS/{username}_pubK.pub')
            os.system(f'chown {username}:{username} /PUBKEYS/{username}_pubK.pub')

            print(f"Private and public keys generated for {username}.")

else:
    print("Current user is not root, please login as root and try again")
