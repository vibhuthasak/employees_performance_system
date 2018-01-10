import xmltodict
from xml.parsers import expat
import sys
import logging
import paramiko
import smtplib
import getpass
import psycopg2
import datetime as dt


def xml_parser(path):
    """
    Generator that parse the config.xml file and return important values
    Arguments: path (Path to the config.xml file) 
    Returns: ip_add, port, usr_name, pwd, email, memory_limit, cpu_limit
    """
    with open(path) as f:
        try:
            document = xmltodict.parse(f.read())
            # Type of the 'document' variable is a OrderedDict
        except expat.ExpatError as e:
            logging.error('XML_PARSING_ERROR : {0} . Please Check {1} file'.format(e, path))
            sys.exit()

    data = document['clients']['client']  # Extract Client Heading information from 'document'
    for i in data:
        # Tags inside client headings can be extracted using the "@tagname" and assign into variables
        ip_add, port, usr_name, pwd, email = i['@ip'], i['@port'], i['@username'], i['@password'], i['@mail']
        memory_limit, cpu_limit = i['alert'][0]['@limit'], i['alert'][1]['@limit']
        yield ip_add, port, usr_name, pwd, email, memory_limit, cpu_limit

# SSH Connection and Receive data


def ssh_connection(ip, port, usr, pwd):
    """ 
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(ip, port=port, username=usr, password=pwd)
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("Unable to connect {0} via port {1}".format(ip, port))
        sys.exit()

    with ssh_client.open_sftp() as sftp:
        sftp.put('Client.py', 'client_script.py')

    stdin, stdout, stderr = ssh_client.exec_command('python client_script.py')

    with ssh_client.open_sftp() as sftp:
        sftp.get('private_key.txt', 'private_key.txt')

    retet = stdout
    ssh_client.close()
    return retet.readlines()

def decrypt_RSA(private_key_loc, package):
    '''
    param: public_key_loc Path to your private key
    param: package String to be decrypted
    return decrypted string
    '''
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP
    key = open(private_key_loc, "r").read()
    rsakey = RSA.importKey(key)
    rsakey = PKCS1_OAEP.new(rsakey)
    decrypted = rsakey.decrypt(package)
    return decrypted


# Email if limits are reached
def send_email(sender_mail, send_mail, pwd, msg):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender_mail, pwd)
        server.sendmail(sender_mail, send_mail, msg)
    finally:
        server.quit()

# Saving to the database


def saving_database(values, database, db_username, db_password, db_host):
    conn = psycopg2.connect(database=database,
                            user=db_username,
                            password=db_password,
                            host=db_host, port="5432")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO machine_data (date, ip_add, memory, cpu) VALUES (233, 'dege', 233, 333)"
    )
    conn.commit()
    conn.close()


def main():
    while True:
        email_servername = input('Email Address: ')
        email_username = input('Email user name: ')
        email_password = getpass.getpass(prompt="Email password: ")
        database_name = input('Database_name: ')
        database_username = input('Database Username: ')
        database_password = getpass.getpass(prompt="Database password: ")
        if (email_servername or email_username or email_password or database_name or database_username or database_password) is '':
            print("Please Enter Valid Data")
            continue
        else:
            break

    for j in xml_parser('config.xml'):
        ip_add = j[0]
        port = j[1]
        usr_name = j[2]
        pwd = j[3]
        ret = ssh_connection(ip_add, port, usr_name, pwd)
        print("Encrypted:", ret)
        drt = decrypt_RSA('private_key.txt', ret)
        print("Decrypted:", drt)

# if __name__ == '__main__':
#     main()

saving_database((12, 30, '192.168.1.2'), 'crossover', 'postgres', 'mjdes', 'localhost')