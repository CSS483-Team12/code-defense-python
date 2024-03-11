import re
import hashlib
import os
import sys

def get_valid_name(prompt):
    while True:
        name = input(prompt)
        if len(name) <= 50 and re.match("^[A-Z][a-z]+$", name):
            return name
        else:
            print("Invalid input. Please enter up to 50 alphabetic characters and spaces.")

def get_valid_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a 4-byte integer value.")

def get_valid_filename(prompt):
    while True:
        filename = input(prompt)
        if filename and len(filename) < 255: # assuming a typical max path length
            return filename
        else:
            print("Invalid filename. Please ensure it is not empty and is shorter than 255 characters.")

def get_password():
    while True:
        password = input("Enter a password: ")
        confirm_password = input("Re-enter your password: ")
        if password == confirm_password:
            return password
        else:
            print("Passwords do not match. Please try again.")

def hash_password(password):
    salt = os.urandom(16)
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000), salt

def write_to_file(output_file, content):
    with open(output_file, 'w') as f:
        for key, value in content.items():
            f.write(f"{key}: {value}\n")

def main():
    first_name = get_valid_name("Enter your first name: ")
    last_name = get_valid_name("Enter your last name: ")
    int1 = get_valid_int("Enter the first integer: ")
    int2 = get_valid_int("Enter the second integer: ")
    input_filename = get_valid_filename("Enter the name of the input file: ")
    output_filename = get_valid_filename("Enter the name of the output file: ")
    
    password = get_password()
    hashed_password, salt = hash_password(password)
    
    # Assuming no overflow, as per requirement. For safety, consider checking or using larger data types
    sum_of_ints = int1 + int2
    product_of_ints = int1 * int2
    
    content_to_write = {
        "First name": first_name,
        "Last name": last_name,
        "First Integer": int1,
        "Second Integer": int2,
        "Sum": sum_of_ints,
        "Product": product_of_ints,
        "Input File Name": input_filename,
        "Input File Contents": ""
    }
    
    try:
        with open(input_filename, 'r') as f:
            content_to_write["Input File Contents"] = f.read()
    except Exception as e:
        print(f"Failed to read from {input_filename}: {e}")
        sys.exit(1)

    write_to_file(output_filename, content_to_write)
    
    # Write hashed password to file (demonstration purpose, normally you'd store this securely)
    with open('password_hash.bin', 'wb') as f:
        f.write(salt + hashed_password)

    print("Information has been successfully written to the output file.")

if __name__ == "__main__":
    main()
