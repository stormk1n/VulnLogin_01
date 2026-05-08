from name_password_checker import login
import base64


name, password = login()


encodedpassword = base64.b64encode(password.encode())

print(f"\nEncoded password is {encodedpassword.decode()}")