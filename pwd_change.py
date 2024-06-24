from getpass import getpass
from PyGeneratePassword import PasswordGenerate
import re
import platform
import subprocess
import os
import mysql.connector
import smtplib
import sys

# Establish a connection
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='rockfall',
    database='internship'
)

def validate_password(password):
    pattern = r'^(?=.*[a-z]|[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}|:<>?/~`])[A-Za-z\d!@#$%^&*()_+{}|:<>?/~`]{8,}$'
    return bool(re.match(pattern, password))

def getCredentials(username):
    # Code to be changed to retrieve credentials from vault
    cursor = connection.cursor()

    # Execute queries
    cursor.execute(f"SELECT * FROM vault where username = \"{username}\"")
    result = cursor.fetchall()
    # username = input("Enter username: ")
    old_password = result[0][3]
    password1 = PasswordGenerate(length=8, use_digits=True, use_special_chars=True)
    email = result[0][2]
    cursor.close()
    return username, old_password, password1, email
    # print("Password requirements:")
    # print(" - Starts with a capital letter")
    # print(" - Contains a digit and special character")
    # print(" - At least 8 characters long\n")
    # while True:
    #     password1 = getpass("Enter new password: ")
    #     password2 = getpass("Confirm new password: ")
    #     if validate_password(password1):
    #         if password1 == password2:
    #             return username, old_password, password1
    #         else:
    #             print("Passwords do not match. Try again.")
    #     else:
    #         print("Invalid password. Try again.")

def set_password_windows(username, old_password, new_password):
    print('Changing password')
    ret = subprocess.call("net user " + username + " " + new_password, shell=True)
    # NetUserChangePassword(None, username, old_password, new_password)
    if ret == 0:
        print('Password reset successfully.')
        return new_password
    else:
        print('Password reset failed.')
        return None

def set_password_linux(username, old_password, new_password):
    process = subprocess.Popen(['sudo','passwd', username], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    #process.stdin.write(current_password.encode() + b'\n')

    process.stdin.write(new_password.encode() + b'\n')

    process.stdin.write(new_password.encode() + b'\n')

    output, error = process.communicate()

    if process.returncode == 0:
        print('Password reset successfully.')
        return new_password
    else:
        print('Password reset failed.', error.decode())
        return None

def send_mail(email, password):
    if password:
        sender = 'riturajpradhan911@gmail.com'

        subject = 'System Password Change'
        message = f'Your password has successfully been changed to {password}.'

        text = f'Subject: {subject}\n\n{message}'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(sender, 'lvcs qbzr rhrt afry')

        server.sendmail(sender, email, text)


def main():
    if len(sys.argv) > 1:
        username = sys.argv[1]
        print(f'received username {username}')
        # Process the arguments as needed
    else:
        print("No arguments provided.")
        return
    new_password = None
    username, old_password, password, email = getCredentials(username)
    if platform.system() == 'Linux':
        new_password = set_password_linux(username, old_password, password)
    elif platform.system() == 'Windows':
        new_password = set_password_windows(username, old_password, password)
    if password:
        cursor = connection.cursor()
        cursor.execute(f'update vault set user_password = "{new_password}" where username = "{username}"')
        connection.commit()
        cursor.close()
        connection.close()
    send_mail(email, new_password)

if __name__ == '__main__':
    main()