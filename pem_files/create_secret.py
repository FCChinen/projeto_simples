import os
import base64

# Generate a random 256-bit secret
secret = base64.b64encode(os.urandom(32))

with open("secret.txt", "wb") as f:
    f.write(secret)
