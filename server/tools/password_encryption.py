#from Crypto.Cipher import AES
#import base64
import hashlib

# secret_key = '1234567890123456' # create new & store somewhere safe
# cipher = AES.new(secret_key,AES.MODE_ECB)

# def encode_password(password):
# 	msg_text = password.rjust(64)
# 	return base64.b64encode(cipher.encrypt(msg_text))

# def decode_password(password_encoded):
# 	return cipher.decrypt(base64.b64decode(password_encoded)).strip()

def encode_password(password):
	h = hashlib.md5(password.encode())
	return h.hexdigest()

# def decode_password(password_encoded):
# 	return base64.b64decode(password_encoded)