#!/usr/bin/env python3
import base64
import sys
import re
from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad

def main():
    if len(sys.argv) != 3:
        print(f"Use: python3 {sys.argv[0]} <des_key> <session_vars>")
        sys.exit(1)

    decryption_key = sys.argv[1]
    base64_string = sys.argv[2]

    try:
        decoded_bytes = base64.b64decode(base64_string)
        decoded_string = decoded_bytes.decode('utf-8')
        
        username = None
        password = None
        
        username_match = re.search(r'username\|s:\d+:"([^"]+)"', decoded_string)
        if username_match:
            username = username_match.group(1)
        
        password_match = re.search(r'password\|s:\d+:"([^"]+)"', decoded_string)
        if password_match:
            password = password_match.group(1)
        
        if password:
            password_bytes = base64.b64decode(password)
            
            iv = password_bytes[:8]
            tc = password_bytes[8:]
            
            # 3DES
            cipher = DES3.new(decryption_key.encode('utf-8'), DES3.MODE_CBC, iv)
            decrypted_password = unpad(cipher.decrypt(tc), DES3.block_size)
            decrypted_password_str = decrypted_password.decode('utf-8')
            print()
            print(f"User: {username}")
            print(f"Password: {decrypted_password_str}")
            print()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()