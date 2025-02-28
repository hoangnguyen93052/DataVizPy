import os
from cryptography.fernet import Fernet

# Generate a key for encryption and decryption
def generate_key():
    """Generate a key for symmetric encryption"""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
        
# Load the previously generated key
def load_key():
    """Load the key from the current directory named 'secret.key'"""
    return open("secret.key", "rb").read()

# Encrypt the data
def encrypt_data(data):
    """Encrypt the data using the loaded key"""
    key = load_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

# Decrypt the data
def decrypt_data(encrypted_data):
    """Decrypt the data using the loaded key"""
    key = load_key()
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data

# Save encrypted data to a file
def save_encrypted_file(filename, data):
    """Save encrypted data to a file"""
    with open(filename, "wb") as file:
        file.write(data)

# Read encrypted data from a file
def read_encrypted_file(filename):
    """Read encrypted data from a given file"""
    with open(filename, "rb") as file:
        return file.read()

# Example Usage
if __name__ == "__main__":
    # Step 1: Generate key for the first time
    if not os.path.exists("secret.key"):
        print("Generating new key...")
        generate_key()
    else:
        print("Key already exists.")
    
    # Step 2: Get user input
    plaintext = input("Enter the message to encrypt: ")
    
    # Step 3: Encrypt the data
    encrypted = encrypt_data(plaintext)
    print(f"Encrypted data: {encrypted}")
    
    # Step 4: Save encrypted data to a file
    save_encrypted_file("encrypted_message.enc", encrypted)
    print("Encrypted data saved to 'encrypted_message.enc'")
    
    # Step 5: Read encrypted data from file
    encrypted_from_file = read_encrypted_file("encrypted_message.enc")
    
    # Step 6: Decrypt the data
    decrypted = decrypt_data(encrypted_from_file)
    print(f"Decrypted data: {decrypted}")

    # Validate that decryption worked correctly
    assert decrypted == plaintext, "Decryption failed. The decrypted text does not match the original text."
    print("Decryption successful. The original text and the decrypted text match.")

# Additional utilities
def list_available_files():
    """List all files in the current directory that can be encrypted or decrypted"""
    return [f for f in os.listdir() if os.path.isfile(f) and not f.endswith('.key')]

def encrypt_file(file_path):
    """Encrypt the contents of a file"""
    with open(file_path, "r") as file:
        file_data = file.read()
    encrypted_data = encrypt_data(file_data)
    save_encrypted_file(file_path + ".enc", encrypted_data)
    print(f"File '{file_path}' encrypted and saved as '{file_path}.enc'")

def decrypt_file(file_path):
    """Decrypt the contents of an encrypted file"""
    encrypted_data = read_encrypted_file(file_path)
    decrypted_data = decrypt_data(encrypted_data)
    with open(file_path.replace(".enc", ""), "w") as file:
        file.write(decrypted_data)
    print(f"File '{file_path}' decrypted and saved as '{file_path.replace('.enc', '')}'")

def main_menu():
    """Display the main menu for file encryption and decryption operations"""
    while True:
        print("\n=== Encryption and Decryption Menu ===")
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. List available files")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            file_path = input("Enter the file path to encrypt: ")
            if os.path.exists(file_path):
                encrypt_file(file_path)
            else:
                print("File not found.")
        elif choice == '2':
            file_path = input("Enter the encrypted file path to decrypt (should end with .enc): ")
            if os.path.exists(file_path):
                decrypt_file(file_path)
            else:
                print("File not found.")
        elif choice == '3':
            files = list_available_files()
            print("Available files:", files)
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()