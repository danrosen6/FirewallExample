import sys  # Import the sys module to interact with the Python runtime environment.
import time  # Import the time module for accessing the current time and managing durations.
from scapy.all import Ether, IP, TCP, sendp  # Import necessary components from Scapy for packet crafting and sending.

# Constants for the script's configuration:
TARGET_IP = "192.168.x.x"  # Target IP address to which the packets will be sent.
INTERFACE = "eth0"  # Network interface through which the packets will be sent.
NUM_PACKETS = 100  # Total number of packets to send.
DURATION = 5  # Duration of the packet sending operation in seconds.

def send_packets(target_ip, interface, num_packets, duration):
    """Send a specified number of TCP packets to a target IP address over a given duration."""
    packet = Ether() / IP(dst=target_ip) / TCP()  # Construct the packet using Ethernet, IP, and TCP layers.
    end_time = time.time() + duration  # Calculate the ending time based on the current time plus the duration.
    packet_count = 0  # Initialize a counter for the number of packets sent.

    while time.time() < end_time and packet_count < num_packets:  # Loop until the time or packet limit is reached.
        sendp(packet, iface=interface)  # Send the packet via the specified network interface.
        packet_count += 1  # Increment the packet count after each packet is sent.

if __name__ == "__main__":
    if sys.version_info[0] < 3:  # Check if the script is being run with Python 3 or newer.
        print("This script requires Python 3.")  # Notify the user that Python 3 is required.
        sys.exit(1)  # Exit the script with a status code of 1 to indicate an error.

    send_packets(TARGET_IP, INTERFACE, NUM_PACKETS, DURATION)  # Call the function to send packets.