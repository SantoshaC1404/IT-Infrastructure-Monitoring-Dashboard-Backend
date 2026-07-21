from app.core.security.security import hash_password

password = "Admin@123"

print(password)
print(len(password.encode()))

print(hash_password(password))
