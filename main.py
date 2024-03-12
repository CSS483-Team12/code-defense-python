import re
import hashlib
import os
import sys

def get_valid_name(prompt):
    while True:
        name = input(prompt)
        if len(name) <= 50 and re.match("^[A-Za-z][a-z]+$", name):
            return name
        print("Invalid input. Please enter up to 50 alphabetic characters and spaces.")

def get_valid_int(prompt):
    while True:
        value = int(input(prompt))
        if -2147483648 <= value <= 2147483648:
            return value
        print("Invalid input. Please enter a 4-byte integer value range in -2,147,483,648 and 2,147,483,647.")

def get_valid_input_filename(prompt):
    while True:
        filename = input(prompt)
        
        if filename and len(filename) < 255 and re.match("^[a-zA-Z0-9_-]+(?:\s[a-zA-Z0-9_-]+)*$", filename): 
            if os.path.exists(filename + ".txt"):
                return filename
            print("Input file do not exist. Please retry.  ")
        else:
            print("Invalid filename. Please ensure it is not empty, no dot and is shorter than 255 characters.")
            
def get_valid_output_filename(prompt):
    while True:
        filename = input(prompt)
        if filename and len(filename) < 255:
            return filename
        print("Invalid filename. Please ensure it is not empty and is shorter than 255 characters.")

def get_password():
    while True:
        password = input("Enter a password: ")
        
        salt_file = "salt.bin"
        with open(salt_file, 'rb') as file:
            salt = file.read()
        
        while True:
            confirm_password = input("Re-enter your password: ")
            hashed_password = hash_password(password, salt)
            hashed_confirm_password = hash_password(confirm_password, salt)
            
            if hashed_password == hashed_confirm_password:
                with open("password.bin", 'wb') as file:
                    file.write(hashed_password)
                return
            print("Passwords do not match. Please try again.")

def hash_password(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

def write_to_file(output_file, content):
    with open(output_file, 'w') as f:
        for key, value in content.items():
            f.write(f"{key}: {value}\n")

def main():
    first_name = get_valid_name("Enter your first name: ")
    last_name = get_valid_name("Enter your last name: ")
    int1 = get_valid_int("Enter the first integer, range in -2,147,483,648 and 2,147,483,647: ")
    int2 = get_valid_int("Enter the second integer, range in -2,147,483,648 and 2,147,483,647: ")
    input_filename = get_valid_input_filename("Enter the name of the input file, 255 chars limit, file has to exist, accept text file only: ")
    output_filename = get_valid_output_filename("Enter the name of the output file, 255 chars limit: ")
    
    get_password()
    
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
    
    # Just for safety, it should never run into error
    try:
        with open(input_filename, 'r') as f:
            content_to_write["Input File Contents"] = f.read()
    except Exception as e:
        print(f"Failed to read from {input_filename}: {e}")
        sys.exit(1)

    write_to_file(output_filename, content_to_write)

    print("Information has been successfully written to the output file.")

if __name__ == "__main__":
    main()
