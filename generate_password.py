from werkzeug.security import generate_password_hash, check_password_hash

password= input("Enter password to hash: ")
print("\n Your hashed password: ")
print(generate_password_hash(password))