from cryptography.fernet import Fernet
import hashlib
import base64
import os

def generate_key(master_password):
    hashed_key = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(hashed_key).decode()

def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

def register_user():
    if os.path.exists("key.key"):
        print("A master password already exists. Cannot register a new user.")
        return

    master_password = input("Enter your master password: ")
    key = generate_key(master_password)
    with open("key.key", "wb") as f:
        f.write(key.encode())
    print("User registered successfully!")

def authenticate_user():
    if not os.path.exists("key.key"):
        print("No master password exists. Please register a user first.")
        return None

    master_password = input("Enter your master password: ")
    hashed_input_key = generate_key(master_password).encode()

    with open("key.key", "rb") as f:
        stored_key = f.read()

    if hashed_input_key == stored_key:
        return hashed_input_key
    else:
        print("Invalid master password. Please try again.")
        return None

def add_pass(key):
    user = input("Username: ")
    passw = input("Password: ")
    encrypted_passw = encrypt_data(passw, key)
    with open("passwords.txt", "a") as b:
        b.write(f"\n{user}|{encrypted_passw.decode()}")

def view_pass(key):
    if not os.path.exists("passwords.txt"):
        print("Passwords file not found. No passwords have been added yet.")
        return

    with open("passwords.txt", "r") as b:
        lines = b.read().split("\n")

    print("   Name\tPassword")
    for i, item in enumerate(lines):
        if item.strip():  # Skip empty lines
            try:
                username, encrypted_passw = item.split('|')
                decrypted_passw = decrypt_data(encrypted_passw.encode(), key)
                print(f"{i}) {username} | {decrypted_passw}")
            except IndexError:
                pass

def remove_pass(index):
    with open("passwords.txt", "r") as b:
        information = b.readlines()

    information.pop(index)
    newinformation = "".join(information)

    with open("passwords.txt", "w") as b:
        b.write(newinformation)

    print("Successfully removed the item from the list.")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Main code
if __name__ == "__main__":
    if not os.path.exists("key.key"):
        print("No master password exists. Please register a user first.")
        register_user()

    key = authenticate_user()
    if key:
        while True:
            clear_screen()
            print("\nMenu:")
            print("1) Add Password")
            print("2) View Passwords")
            print("3) Remove Password")
            print("4) Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                add_pass(key)
            elif choice == '2':
                view_pass(key)
            elif choice == '3':
                index = int(input("Enter the index of the password to remove: "))
                remove_pass(index)
            elif choice == '4':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
            input("Press Enter to continue...")
