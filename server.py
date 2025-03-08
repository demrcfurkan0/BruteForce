from flask import Flask, render_template, request, jsonify
import hashlib
import itertools
import string
import time
import os

app = Flask(__name__)


# Hashing Function
def hash_password(password, algorithm='sha256'):
    hash_func = getattr(hashlib, algorithm)
    return hash_func(password.encode()).hexdigest()


# Dictionary Attack
def dictionary_attack(hash_to_crack, wordlist="rockyou.txt", algorithm='sha256'):
    try:
        with open(wordlist, 'r', encoding="latin-1") as file:
            for word in file:
                word = word.strip()
                if hash_password(word, algorithm) == hash_to_crack:
                    return word
    except FileNotFoundError:
        return None
    return None


# Brute-Force Attack
def brute_force_attack(hash_to_crack, max_length=3, algorithm='sha256'):
    chars = string.ascii_letters + string.digits + string.punctuation
    for length in range(1, max_length + 1):
        for combination in itertools.product(chars, repeat=length):
            attempt = ''.join(combination)
            if hash_password(attempt, algorithm) == hash_to_crack:
                return attempt
    return None


# Hybrid Attack (Dictionary + Common Variations)
def hybrid_attack(hash_to_crack, wordlist="rockyou.txt", algorithm='sha256'):
    common_variations = ["123", "!", "@", "2024", "password", "1", "01"]

    try:
        with open(wordlist, 'r', encoding="latin-1") as file:
            for word in file:
                word = word.strip()
                if hash_password(word, algorithm) == hash_to_crack:
                    return word

                for variation in common_variations:
                    modified_word = word + variation
                    if hash_password(modified_word, algorithm) == hash_to_crack:
                        return modified_word
    except FileNotFoundError:
        return None
    return None


# Rule-Based Attack
def rule_based_attack(hash_to_crack, wordlist="rockyou.txt", algorithm='sha256'):
    substitutions = {
        'a': ['@', '4'],
        's': ['$', '5'],
        'o': ['0'],
        'i': ['1', '!'],
        'e': ['3']
    }

    try:
        with open(wordlist, 'r', encoding="latin-1") as file:
            for word in file:
                word = word.strip()
                if hash_password(word, algorithm) == hash_to_crack:
                    return word

                mutated_words = [word]
                for char, replacements in substitutions.items():
                    for replacement in replacements:
                        mutated_words.append(word.replace(char, replacement))

                for mutated_word in mutated_words:
                    if hash_password(mutated_word, algorithm) == hash_to_crack:
                        return mutated_word
    except FileNotFoundError:
        return None
    return None


# Mask Attack (Pattern-Based)
def mask_attack(hash_to_crack, mask="????123", algorithm='sha256'):
    chars = {
        "?": string.ascii_lowercase,
        "D": string.digits,
        "L": string.ascii_letters
    }

    possible_chars = [chars.get(char, char) for char in mask]

    for combination in itertools.product(*possible_chars):
        attempt = ''.join(combination)
        if hash_password(attempt, algorithm) == hash_to_crack:
            return attempt
    return None


# Rainbow Table Attack
def generate_rainbow_table(wordlist="rockyou.txt", output_file="rainbow_table.txt", algorithm='sha256'):
    with open(wordlist, 'r', encoding="latin-1") as file, open(output_file, 'w') as out:
        for word in file:
            word = word.strip()
            hashed = hash_password(word, algorithm)
            out.write(f"{hashed} {word}\n")


def rainbow_table_attack(hash_to_crack, table_file="rainbow_table.txt"):
    try:
        with open(table_file, 'r') as file:
            for line in file:
                hashed, word = line.strip().split()
                if hashed == hash_to_crack:
                    return word
    except FileNotFoundError:
        return None
    return None


# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/crack', methods=['POST'])
def crack():
    password = request.form['password']
    attack_type = request.form['attack_type']
    max_length = int(request.form.get('max_length', 3))
    mask_pattern = request.form.get('mask_pattern', "????123")

    hashed_password = hash_password(password)

    start_time = time.time()

    if attack_type == "dictionary":
        result = dictionary_attack(hashed_password)
    elif attack_type == "brute-force":
        result = brute_force_attack(hashed_password, max_length)
    elif attack_type == "hybrid":
        result = hybrid_attack(hashed_password)
    elif attack_type == "rule-based":
        result = rule_based_attack(hashed_password)
    elif attack_type == "mask":
        result = mask_attack(hashed_password, mask_pattern)
    elif attack_type == "rainbow":
        result = rainbow_table_attack(hashed_password)
    else:
        result = None

    end_time = time.time()

    return jsonify({
        "method": attack_type,
        "password": result,
        "time": end_time - start_time
    })


if __name__ == '__main__':
    app.run(debug=True)