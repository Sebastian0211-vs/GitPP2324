import paramiko

# List of IP addresses
ip_addresses = ["172.16.1.2", "172.16.2.2", "172.16.3.2"]

# SSH credentials
username = "pi"  # Replace with your SSH username
password = "pi"  # Replace with your SSH password

def reboot_raspberry_pi(ip):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the Raspberry Pi
        ssh.connect(ip, username=username, password=password)
        
        # Execute the reboot command
        stdin, stdout, stderr = ssh.exec_command("sudo reboot")
        
        # Print the output and errors
        print(f"Rebooting {ip}:")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        # Close the connection
        ssh.close()
    except Exception as e:
        print(f"Failed to reboot {ip}: {e}")

# Reboot all Raspberry Pi devices
for ip in ip_addresses:
    reboot_raspberry_pi(ip)
