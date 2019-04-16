#from Crypto.Cipher import AES
import base64

# secret_key = '1234567890123456' # create new & store somewhere safe
# cipher = AES.new(secret_key,AES.MODE_ECB)

# def encode_password(password):
# 	msg_text = password.rjust(64)
# 	return base64.b64encode(cipher.encrypt(msg_text))

# def decode_password(password_encoded):
# 	return cipher.decrypt(base64.b64decode(password_encoded)).strip()

def encode_password(password):
	return base64.b64encode(password)

def decode_password(password_encoded):
	return base64.b64decode(password_encoded)