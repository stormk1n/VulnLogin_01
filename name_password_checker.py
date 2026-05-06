def get_user_credentials():
    name = input("Enter your name here: ")
    password= input("\nEnter your password here: ")
    
    while len(password) < 8:
        print("\nYour password is too short, make it stronger")
        password = input("\nEnter a stronger password: ")
    
    print("\nEverything is fine, you may proceed")
    return name, password
