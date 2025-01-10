import os

# Open the 'names.txt' file in read mode
with open('names.txt', 'r') as f:
    # Loop through each line in the file
    for line in f:
        # Split the line into username and password based on the comma separator
        username, password = line.strip().split(',')

        # Delete the user and their home directory
        os.system(f'userdel -r {username}')
        # Remove the user's public key file from the /PUBKEYS directory
        os.system(f'rm /PUBKEYS/{username}_pubK.pub')

# Remove the /PUBKEYS directory after deleting all user keys
os.system('rmdir /PUBKEYS')