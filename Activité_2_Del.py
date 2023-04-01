import os

with open('names.txt', 'r') as f:
    for line in f:
        username, password = line.strip().split(',')

        os.system(f'userdel -r {username}')
        os.system(f'rm /PUBKEYS/{username}_pubK.pub')

os.system('rmdir /PUBKEYS')

