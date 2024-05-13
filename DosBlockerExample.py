import os  # Used for executing a shell command
import sys  # Used for accessing system-specific parameters and functions
import time  # Used for time-related functions
from collections import defaultdict  # Import defaultdict to handle default values for dictionary keys
from scapy.all import sniff, IP  # Import functions from Scapy for packet sniffing and manipulation

THRESHOLD = 40  # Define a threshold for packet rate (packets per second)
print(f"THRESHOLD: {THRESHOLD}")  # Print the threshold to the console

def packet_callback(packet):
    """Callback function that processes each sniffed packet."""
    src_ip = packet[IP].src  # Extract the source IP address from the packet
    packet_count[src_ip] += 1  # Increment the packet count for this IP
    current_time = time.time()  # Get the current time
    time_interval = current_time - start_time[0]  # Calculate the elapsed time since the last reset

    if time_interval >= 1:  # Check if one second has passed
        for ip, count in packet_count.items():
            packet_rate = count / time_interval  # Calculate the packet rate
            if packet_rate > THRESHOLD and ip not in blocked_ips:  # Check if the rate exceeds the threshold and IP not already blocked
                print(f"Blocking IP: {ip}, packet rate: {packet_rate}")  # Print the blocking action
                os.system(f"iptables -A INPUT -s {ip} -j DROP") # Block IP using iptables, specific to Unix/Linux
                blocked_ips.add(ip)  # Add the IP to the set of blocked IPs

        packet_count.clear()  # Reset the packet count dictionary
        start_time[0] = current_time  # Reset the start time


if __name__ == "__main__":

    if os.geteuid() != 0: #Checks if user has root privileges
        print("This script requires root privileges.")
        sys.exit(1)

    packet_count = defaultdict(int)  # Initialize a defaultdict to count packets per IP
    start_time = [time.time()]  # Initialize start time for measuring intervals
    blocked_ips = set()  # Initialize a set to keep track of blocked IPs

    print("Monitoring network traffic...")  # Print a status message
    sniff(filter="ip", prn=packet_callback)  # Start sniffing IP packets and use the callback for processing