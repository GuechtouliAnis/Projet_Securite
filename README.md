# Encryption and Signing System

This repository contains Python scripts for encrypting, signing, sending, receiving, and verifying messages using OpenSSL. The system ensures secure communication by utilizing public-key cryptography and digital signatures.

## Features
- **User Account Management**: Automatically creates user accounts and manages public/private keys.
- **Message Encryption**: Encrypts messages using the recipient's public key.
- **Digital Signatures**: Signs encrypted messages using the sender's private key.
- **Message Verification**: Verifies the integrity of received messages by checking digital signatures.

## Prerequisites
- **Linux OS**: The scripts use Linux-specific commands.
- **OpenSSL**: Ensure OpenSSL is installed on your system.
- **Root Access**: Some operations require root permissions.

## Installation
Clone the repository and install the required modules:
```bash
git clone https://github.com/GuechtouliAnis/Projet_Securite
cd Projet_Securite
pip install -r requirements.txt
```

## Usage
1. **Activité 1 (User Creation and Key Management)**:
   - Run this script to create users and generate their public/private key pairs from `names.txt`.
   - Public keys are stored in `/PUBKEYS`, and private keys are stored in each user's `/home/{username}/KEYS` directory.

2. **Activité 2 Del (User Deletion)**:
   - Run this script to delete user accounts and their associated keys.

3. **Activité 2 (Encryption and Message Sending)**:
   - This script encrypts a message using the recipient's public key and signs it with the sender's private key.
   - The encrypted and signed message is saved as `message.bin` and sent to the recipient.

4. **Activité 3 rec (Message Receiving and Verification)**:
   - This script waits for an incoming message, verifies the digital signature, and ensures the message integrity.
   - The decrypted message is saved in `decrypted_message.txt`.

5. **Activité 3 sen (Message Sending with Encryption and Signing)**:
   - This script allows a user to send an encrypted and signed message to another user.

## Folder Structure
```
/
├── names.txt            # Contains usernames and passwords
├── requirements.txt     # Lists required Python modules
├── Activité 1.py        # Script for user creation and key management
├── Activite 2 Del.py    # Script for user deletion
├── Activité 2.py        # Script for message encryption and sending
├── Activité 3 rec.py    # Script for message receiving and verification
├── Activité 3 sen.py    # Script for sending encrypted and signed messages
├── Graph.png            # Graphical representation of encryption time
└── README.md            # Project documentation
```

## Security Considerations
- Store private keys securely with appropriate permissions.
- Ensure the `names.txt` file is protected to avoid exposing user credentials.

## License
This project is licensed under the MIT License.
