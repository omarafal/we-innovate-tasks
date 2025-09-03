from random import randint
import time
import sys
import os

def rand_mac():
    final_addr = "02"

    for _ in range(0, 5):
        final_addr += f":{randint(0, 255):02X}"

    return final_addr

def main(intf):
    try:
        with open(f"/sys/class/net/{intf}/address") as file:
            org = file.read().strip()

        # store in temp file just in case
        with open("./spoof.tmp", "w") as file:
            file.write(org)
    except:
        print("This is not a valid interface.\n")
        sys.exit(1)

    try:
        while True:
            new_add = rand_mac()

            os.system(f"sudo ip link set dev {intf} down")
            os.system(f"sudo ip link set dev {intf} address {new_add}")
            os.system(f"sudo ip link set dev {intf} up")

            print("\nMAC address changed.\n")
            print(f"Running: ip link show {intf}\n")
            os.system(f"ip link show {intf}\n")
            time.sleep(60*3)

    except KeyboardInterrupt:
        print("\nCleaning up before exiting.\nResetting MAC address.")

        try:
            os.system(f"sudo ip link set dev {intf} down")
            os.system(f"sudo ip link set dev {intf} address {org}")
            os.system(f"sudo ip link set dev {intf} up")
        except:
            print("Something went wrong.\n")
            sys.exit(1)
        # to protect the temp file just in case
        if os.path.exists("./spoof.tmp"):
            os.remove("./spoof.tmp")

if __name__ == "__main__":
    try:
        intf = sys.argv[1] # grab interface
    except IndexError:
        print("Usage: python macspoof.py [INTERFACE]\n")
        sys.exit(1)

    main(intf)