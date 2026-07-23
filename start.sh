#!/usr/bin/env bash

checkBcrypt(){
    printf "[+] Checking if bcrypt is on the system\n\n"

    if python3 -c 'import bcrypt' 2>/dev/null; then
        echo '[+] Bcrypt already installed. Skipping....'
    else
        echo '[-] Bcrypt not found'
        echo '[+] Installing with python3 -m pip install bcrypt --user'
        python3 -m pip install bcrypt --user
    fi
}

checkBcrypt

echo '[+] Starting lab: VulnLogin01!'

python3 ./AppCode/flaskbackend.py