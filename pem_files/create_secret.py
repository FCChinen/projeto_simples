import os
import base64

# secret = base64.b64encode(os.urandom(32))

# with open("secret.txt", "wb") as f:
#     f.write(secret)

secret = base64.b64encode(os.urandom(32))

with open("user_pwd_secret.txt", "wb") as f:
    f.write(secret)
