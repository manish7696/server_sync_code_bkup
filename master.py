# import subprocess
# import os
# import time

# # Define the paths to the directories containing the scripts
# directory1 = os.path.expanduser("/home/usrp/Desktop/folder1")
# directory2 = os.path.expanduser("/home/usrp/Desktop/folder2")

# # Define the paths to the scripts
# script1 = os.path.join(directory1, "ffind.py")
# script2 = os.path.join(directory2, "ffind.py")

# # Run the scripts using subprocess
# process1 = subprocess.Popen(["python3", script1], cwd=directory1)
# process2 = subprocess.Popen(["python3", script2], cwd=directory2)

# # Wait for 10 seconds
# time.sleep(9)

# # Terminate the processes
# process1.terminate()
# process2.terminate()

# # Optionally, wait for the processes to terminate properly
# process1.wait()
# process2.wait()

# print("Both scripts have been terminated after 10 seconds.")


import subprocess
import os
import time
import socket
import json

# Define the paths to the directories containing the scripts
directory1 = os.path.expanduser("/home/usrp/Desktop/folder1")
directory2 = os.path.expanduser("/home/usrp/Desktop/folder2")

# Define the paths to the scripts
remote_script1 = os.path.join(directory1, "ffind.py")
remote_script2 = os.path.join(directory2, "ffind.py")

remote_host1 = "kali@192.168.29.79"  # Replace with your remote PC's IP and username
remote_host2 = "ktk@192.168.29.110"  # Replace with your second remote PC's IP and username

# Launch both scripts using subprocess (do not wait yet)
#process1 = subprocess.Popen(["python3", script1], cwd=directory1)
#process2 = subprocess.Popen(["python3", script2], cwd=directory2)

process1 = subprocess.Popen(["ssh", remote_host1, "python3", remote_script1])
process2 = subprocess.Popen(["ssh", remote_host2, "python3", remote_script2])

master_ip = "127.0.0.1"  
master_port = 5005

usrp1_ip = "192.168.29.79"  
usrp2_ip = "192.168.29.110"  
usrp_port1 = 5006
usrp_port2 = 5007
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((master_ip, master_port))

start_times = []

while len(start_times) < 2:  # Expecting messages from 2 USRPs
    data, addr = sock.recvfrom(1024)  # Buffer size of 1024 bytes
    start_time_message = json.loads(data.decode())
    print(f"Received start time from {addr}: {start_time_message['start_time']}")
    start_times.append(start_time_message['start_time'])


print(f"Start times from both USRPs: {start_times}")

max_start_time = max(start_times)

# Add 5 seconds to the max start time
new_start_time = max_start_time + 5

# Send the new start time to both USRPs
new_start_time_message = json.dumps({"start_time": new_start_time}).encode()

sock.sendto(new_start_time_message, (usrp1_ip, usrp_port1))
sock.sendto(new_start_time_message, (usrp2_ip, usrp_port2))

print(f"New start time {new_start_time} sent to both USRPs")

# # Allow both scripts some time to initialize and synchronize with the PPS signal
# time.sleep(1)

# Wait for 9 seconds to capture data (the scripts will start recording simultaneously on the PPS pulse)
time.sleep(9)

# Terminate both processes after data capture
process1.terminate()
process2.terminate()

# Optionally, wait for the processes to terminate properly
process1.wait()
process2.wait()

print("Both scripts have been terminated after 10 seconds.")
