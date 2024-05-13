import os  # Used for executing a shell command
import sys  # Used for accessing system-specific parameters and functions
import time  # Used for time-related functions
from collections import defaultdict  # Import defaultdict to handle default values for dictionary keys
from scapy.all import sniff, IP  # Import functions from Scapy for packet sniffing and manipulation
import ctypes  # Allows calling functions of C libraries or Windows API

THRESHOLD = 40  # Define a threshold for packet rate (packets per second)
print(f"THRESHOLD: {THRESHOLD}")  # Print the threshold to the console

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()  # Attempt to use Windows API to check admin status
    except:
        return False  # Return False if any exception occurs during the check

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
                 # Using netsh command to block the IP on Windows
                os.system(f"netsh advfirewall firewall add rule name=\"Block {ip}\" dir=in interface=any action=block remoteip={ip}")
                blocked_ips.add(ip)  # Add the IP to the set of blocked IPs

        packet_count.clear()  # Reset the packet count dictionary
        start_time[0] = current_time  # Reset the start time

def is_admin():
    """Function to check if the current script is run as an administrator."""
    try:
        # Attempt to call a Windows API function that checks for administrator privileges.
        # `IsUserAnAdmin` returns 1 if the script is running with admin privileges, otherwise 0.
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        # If the call fails (e.g., due to lack of permissions), catch the exception and return False.
        return False

if __name__ == "__main__":

    # This condition checks if the script is being run as the main module and not being imported.
    if not is_admin():
        # If not running as admin, use the ShellExecuteW function to request admin privileges.
        # Parameters:
        # 1. None: The handle to the parent window, None means no parent.
        # 2. "runas": Verb used to execute the program as administrator.
        # 3. sys.executable: The executable to launch, here it's Python itself.
        # 4. " ".join(sys.argv): Command-line arguments for the script, joined by spaces.
        #    This includes the script name and any arguments passed to it.
        # 5. None: Default directory, None uses the current directory.
        # 6. 1: Show command used to display the window (1 means normal window).
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    packet_count = defaultdict(int)  # Initialize a defaultdict to count packets per IP
    start_time = [time.time()]  # Initialize start time for measuring intervals
    blocked_ips = set()  # Initialize a set to keep track of blocked IPs

    print("Monitoring network traffic...")  # Print a status message
    sniff(filter="ip", prn=packet_callback)  # Start sniffing IP packets and use the callback for processing
