import random  # Imports the random module used for generating random numbers

def generate_random_ip():
    # Generates a random IP address within a specific range, here 192.168.1.0 to 192.168.1.20
    return f"192.168.1.{random.randint(0, 20)}"

def check_firewall_rules(ip, rules):
    # This function checks if a given IP address should be blocked based on a set of rules.
    # ip: the IP address to check
    # rules: a dictionary of IP addresses and corresponding actions (e.g., "block")

    for rule_ip, action in rules.items():  # Loop through each entry in the rules dictionary
        # rule_ip: an IP address from the rules dictionary
        # action: the action ("block") associated with the rule_ip

        if ip == rule_ip:  # Check if the input IP matches this rule's IP
            return action  # If there's a match, return the action to be taken (e.g., "block")

    return "allow"  # If no rules match the input IP, return "allow"

def main():
    # Defines a set of firewall rules where certain IPs are explicitly blocked
    firewall_rules = {
        "192.168.1.1": "block",
        "192.168.1.4": "block",
        "192.168.1.9": "block",
        "192.168.1.13": "block",
        "192.168.1.16": "block",
        "192.168.1.19": "block"
    }

    for _ in range(12):  # Runs the test 12 times
        ip_address = generate_random_ip()  # Generates a random IP address
        action = check_firewall_rules(ip_address, firewall_rules)  # Checks what action to take for the IP
        random_number = random.randint(0, 9999)  # Generates a random number for demonstration
        print(f"IP: {ip_address}, Action: {action}, Random: {random_number}")

if __name__ == "__main__":
    # Main entry point of the program; main() is called only when the script is executed directly
    main()
