import subprocess
with open ("names.txt", "r") as f:
    names = f.readlines()
subprocess.run(["sudo","su"])
subprocess.run(["cd","/"])
subprocess.run(["mkdir","PUBKEYS"])
for name in names:
    username = name.strip().lower().replace(" ","")
    subprocess.run(["useradd","-m",username])

    print(f"User {username} generated")
    print(f"Generating private key for the user...")
    subprocess.run(["openssl","genrsa","-aes128","-out",f"/home/{username}/KEYS/{username}_private.pem","1024"])
    print(f"Private Key generated for user {username} successfully and is in /KEYS")
    print(f"Generating public key for the user...")
    subprocess.run(["openssl","rsa","-in",f"{username}_private.pem","-pubout",">",f"{username}_public.pub"])
    subprocess.run(["cp",f"{username}_public.pub",f"/home/{username}/KEYS"])
    subprocess.run(["cp",f"{username}_public.pub","/PUBKEYS"])
    subprocess.run(["rm",f"{username}_public.pub"])
    print(f"Public Key generated for user {username} successfully and is in /KEYS and /PUBKEYS")
