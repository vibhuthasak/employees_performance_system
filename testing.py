# # Execute and Recieve system level details and return encrypted.
# # import psutil
# #
# # print(psutil.virtual_memory().percent)
# # total_cpu_usage = psutil.cpu_percent(interval=0.5, percpu=True)
# # avg_cpu_usage = sum(total_cpu_usage)/len(total_cpu_usage)
# # print(avg_cpu_usage)
#
# def generate_RSA(bits=2048):
#     '''
#     Generate an RSA keypair with an exponent of 65537 in PEM format
#     param: bits The key length in bits
#     Return private key and public key
#     '''
#     pvt_file = open('private_key.txt', 'wb')
#     pub_file = open('public_key.txt', 'wb')
#     from Crypto.PublicKey import RSA
#     new_key = RSA.generate(bits, e=65537)
#     public_key = new_key.publickey().exportKey("PEM")
#     private_key = new_key.exportKey("PEM")
#     pvt_file.write(private_key)
#     pub_file.write(public_key)
#     return private_key, public_key
#
#
# def encrypt_RSA(public_key_loc, message):
#     '''
#     param: public_key_loc Path to public key
#     param: message String to be encrypted
#     return base64 encoded encrypted string
#     '''
#     from Crypto.PublicKey import RSA
#     from Crypto.Cipher import PKCS1_OAEP
#     key = open(public_key_loc, "r").read()
#     rsakey = RSA.importKey(key)
#     rsakey = PKCS1_OAEP.new(rsakey)
#     encrypted = rsakey.encrypt(message)
#     return encrypted
#
#
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
#
# generate_RSA()
# massage = b'hello from the other size'
# er = encrypt_RSA('public_key.txt', message=massage)
# print(er)
#
# rf = decrypt_RSA('private_key.txt', er)
# print(rf)

a = ['A','A','B','C','D','D','B','B','B','E','A']

# prev_letter = a[0]
# counter = 0
# dicto = {}
#
# for i in a[1:]:
#     print(i)
#     if i == prev_letter:
#         counter += 1
#     if i != prev_letter:
#         counter += 1
#         try:
#             dicto.update({prev_letter:counter})
#             counter = 0
#         except KeyError:
#             if dicto[prev_letter] > counter:
#                 dicto[prev_letter] = counter
#                 counter = 0
#             else:
#                 counter = 0
#     print(counter)
#     prev_letter = i
# print(dicto)

prev_letter = None
max_count = 0
max_letter = None
count = 0

for i in a:
    if i == prev_letter:
        count += 1

    else:
        count = 1

    if count > max_count:
        max_count = count
        max_letter = i

    prev_letter = i

print(max_count, max_letter)
