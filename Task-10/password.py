import secrets
import string

length = int(input("Password length: "))

chars = string.ascii_letters + string.digits + "!@#$%^&*"
password = "".join(secrets.choice(chars) for _ in range(length))

print("\nGenerated password:")
print(password)