# Execute and Recieve system level details and return encrypted.

import psutil

memory_usage = psutil.virtual_memory().percent
total_cpu_usage = psutil.cpu_percent(interval=0.5, percpu=True)
avg_cpu_usage = sum(total_cpu_usage)/len(total_cpu_usage)

def generate_RSA(bits=2048):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    pvt_file = open('private_key.txt', 'wb')
    pub_file = open('public_key.txt', 'wb')
    from Crypto.PublicKey import RSA
    new_key = RSA.generate(bits, e=65537)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")
    pvt_file.write(private_key)
    pub_file.write(public_key)
    return private_key, public_key


def encrypt_RSA(public_key_loc, message):
    '''
    param: public_key_loc Path to public key
    param: message String to be encrypted
    return base64 encoded encrypted string
    '''
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP
    key = open(public_key_loc, "r").read()
    rsakey = RSA.importKey(key)
    rsakey = PKCS1_OAEP.new(rsakey)
    encrypted = rsakey.encrypt(message)
    return encrypted

# def decrypt_RSA(private_key_loc, package):
#     '''
#     param: public_key_loc Path to your private key
#     param: package String to be decrypted
#     return decrypted string
#     '''
#     from Crypto.PublicKey import RSA
#     from Crypto.Cipher import PKCS1_OAEP
#     from base64 import b64decode
#     key = open(private_key_loc, "r").read()
#     rsakey = RSA.importKey(key)
#     rsakey = PKCS1_OAEP.new(rsakey)
#     decrypted = rsakey.decrypt(package)
#     return decrypted

generate_RSA()
message = bytes(str(memory_usage) + ',' + str(avg_cpu_usage), 'utf-8')
er = encrypt_RSA('public_key.txt', message=message)
print(er)