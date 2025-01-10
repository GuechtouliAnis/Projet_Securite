import os

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