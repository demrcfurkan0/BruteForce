import hashlib
import itertools
import string
import time

def hash_password(password, algorithm='sha256'):
    hash_func = getattr(hashlib, algorithm)
    return hash_func(password.encode()).hexdigest()

def dictionary_attack(hash_to_crack, wordlist, algorithm='sha256'):
    try:
        with open(wordlist, 'r', encoding="latin-1") as file:  # Some wordlists use latin-1 encoding
            for word in file:
                word = word.strip()
                if hash_password(word, algorithm) == hash_to_crack:
                    return word
    except FileNotFoundError:
        print(f"Error: Wordlist file '{wordlist}' not found.")
    return None

def brute_force_attack(hash_to_crack, max_length, algorithm='sha256'):
    chars = string.ascii_letters + string.digits + string.punctuation
    for length in range(1, max_length + 1):
        for combination in itertools.product(chars, repeat=length):
            attempt = ''.join(combination)
            if hash_password(attempt, algorithm) == hash_to_crack:
                return attempt
    return None

# User-defined password
password = "123"
hashed_password = hash_password(password)

# Dictionary Attack
start_time = time.time()
wordlist_file = "rockyou.txt"  # Change this to any other wordlist file you want to use
result = dictionary_attack(hashed_password, wordlist_file)
end_time = time.time()

if result:
    print(f"Password cracked (Dictionary Attack): {result}")
else:
    print(f"Dictionary attack failed. Trying brute-force...")

    # Brute-Force Attack
    start_time = time.time()
    result = brute_force_attack(hashed_password, max_length=3)  # Adjust length accordingly
    end_time = time.time()

    if result:
        print(f"Password cracked (Brute-Force Attack): {result}")
    else:
        print(f"Brute-force attack failed.")

print(f"Total Time taken: {end_time - start_time} seconds.")