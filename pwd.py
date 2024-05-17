from getpass import getpass
from win32security import LogonUser
from win32con import LOGON32_LOGON_INTERACTIVE, LOGON32_PROVIDER_DEFAULT
from win32net import NetUserChangePassword, error
import re

def validate_password(password):
    pattern = r'^(?=.*[a-z]|[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}|:<>?/~`])[A-Za-z\d!@#$%^&*()_+{}|:<>?/~`]{8,}$'
    return bool(re.match(pattern, password))

def getCredentials():
    # Code to be changed to retrieve credentials from vault
    username = input("Enter username: ")
    old_password = input("Enter old password")
    print("Password requirements:")
    print(" - Starts with a capital letter")
    print(" - Contains a digit and special character")
    print(" - At least 8 characters long\n")
    while True:
        password1 = getpass("Enter new password: ")
        password2 = getpass("Confirm new password: ")
        if validate_password(password1):
            if password1 == password2:
                return username, old_password, password1
            else:
                print("Passwords do not match. Try again.")
        else:
            print("Invalid password. Try again.")

def set_password(username, old_password, new_password):
    try:
        print('Changing password')
        NetUserChangePassword(None, username, old_password, new_password)
    except error:
        print("Failed to change password")

def verify_success(username, password):
    try:
        LogonUser(username, None, password, LOGON32_LOGON_INTERACTIVE, LOGON32_PROVIDER_DEFAULT)
    except:
        return False
    return True

def main():
    username, old_password, password = getCredentials()
    set_password(username, old_password, password)
    if verify_success(username, password):
        print ('Password reset successfully.')
    else:
        print ('Password reset failed.')

if __name__ == '__main__':
    main()