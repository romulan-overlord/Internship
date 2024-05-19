import subprocess
def change_system_password(username, current_password, new_password):
    process = subprocess.Popen(['sudo','passwd', username], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    #process.stdin.write(current_password.encode() + b'\n')

    process.stdin.write(new_password.encode() + b'\n')

    process.stdin.write(new_password.encode() + b'\n')

    output, error = process.communicate()

    if process.returncode == 0:
        print('syccess')
    else:
        print('fail', error.decode())

change_system_password('romulan', 'omsrisairam', 'omsrisairam')