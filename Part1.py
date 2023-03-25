import subprocess

# Run the `ls` command and print its output
output = subprocess.run(['ls', '-al'], capture_output=True, text=True)
print(output.stdout)
