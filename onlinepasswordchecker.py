import hashlib
import requests

# Checks if a password is in known data breaches using part of its hashed value
def is_compromised(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    # Sends first 5 characters of the hash to the online breach database (privacy-safe)
    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")

    if response.status_code != 200:
        print("Error contacting breach database.")
        return

    # Looks through matching hash endings returned by the API
    matches = (line.split(":") for line in response.text.splitlines())
    for h, count in matches:
        if h == suffix:
            print(f"Found in {count} breaches.")
            return

    print("Not found in any known breach.")

# Keeps asking the user for passwords until they type 'exit' or press Ctrl+C
if __name__ == "__main__":
    try:
        while True:
            pw = input("Password to check (or 'exit'): ").strip()
            if pw.lower() == "exit":
                break
            is_compromised(pw)
            print()
    except KeyboardInterrupt:
        print("\nGoodbye.")
