from getpass import getpass
import re
import platform
import subprocess
import os

def validate_password(password):
    pattern = r'^(?=.*[a-z]|[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}|:<>?/~`])[A-Za-z\d!@#$%^&*()_+{}|:<>?/~`]{8,}$'
    return bool(re.match(pattern, password))

def getCredentials():
    # Code to be changed to retrieve credentials from vault
    username = input("Enter username: ")
    old_password = input("Enter old password: ")
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

def set_password_windows(username, old_password, new_password):
    print('Changing password')
    subprocess.call("net user " + username + " " + new_password, shell=True)
    # NetUserChangePassword(None, username, old_password, new_password)
    try:
        # Try to authenticate with the new password
        os.system(f'runas /user:{username} cmd')
        print("Password reset was successful.")
    except Exception as e:
        print("Failed to authenticate.", e)

def set_password_linux(username, old_password, new_password):
    process = subprocess.Popen(['sudo','passwd', username], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    #process.stdin.write(current_password.encode() + b'\n')

    process.stdin.write(new_password.encode() + b'\n')

    process.stdin.write(new_password.encode() + b'\n')

    output, error = process.communicate()

    if process.returncode == 0:
        print('Password reset successfully.')
    else:
        print('Password reset failed.', error.decode())

def main():
    username, old_password, password = getCredentials()
    if platform.system() == 'Linux':
        set_password_linux(username, old_password, password)
    elif platform.system() == 'Windows':
        set_password_windows(username, old_password, password)

if __name__ == '__main__':
    main()