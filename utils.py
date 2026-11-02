import random
import re

def read_proxies_from_file(file_path):
    proxies = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Assuming each line in the file contains a proxy in the format IP:Port
                proxy = line.strip()
                proxies.append(proxy)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return proxies

def extract_login_code(text):
    # Define a regular expression pattern to match the login code
    pattern = re.compile(r'Login code\n(\d+)')
    match = pattern.search(text)
    if match:
        return match.group(1)
    else:
        return None
    
def generate_random_email():
    # Generate 12 random digits
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(12)])

    # Construct the email address
    email = f"{random_digits}@yopmail.com"

    with open('mails.txt', 'a') as file:
        file.write(email + '\n')
    return email