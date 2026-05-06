from name_password_checker import get_user_credentials
import base64


name, password = get_user_credentials()


encodedpassword = base64.b64encode(password.encode())

print(f"\nEncoded password is {encodedpassword.decode()}")