import ssl
import OpenSSL
import datetime
from datetime import date
import jks
from OpenSSL import crypto
import constant
import glob


_ASN1 = OpenSSL.crypto.FILETYPE_ASN1

#Print msg in console about certs
# 
def print_msg(cn,path,days):
    msg = 'NA'
    if(days >= constant.WARN_THRESHOLD):
        msg = 'INFO'
        print("INFO: CN: ", cn, "| Path: ", path, "| Days: ", days)
    elif(days <= constant.ERROR_THRESHOLD):
        msg = 'ERROR'
        print("ERROR: CN: ", cn, "| Path: ", path, "| Days: ", days)
    elif(days <= constant.WARN_THRESHOLD):
        msg = 'WARN'
        print("WARN: CN: ", cn, "| Path: ", path, "| Days: ", days)
    return msg

#Get certificate info from remote urls.
# 
def get_remote_expiry_days(cert_info):
    cert_expire_data = {}
    cert = ssl.get_server_certificate((cert_info['path'],cert_info['port']))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    common_name = x509.get_subject().commonName
    time_to_expire = datetime.datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ').strftime('%s')
    current_time = datetime.date.today().strftime('%s')
    days_left = int(time_to_expire) - int(current_time)
    cert_expire_data[common_name]=int(days_left/(60*60*24))
    print_msg(common_name,cert_info['path'], int(days_left/(60*60*24)))
    return cert_expire_data 

#Get certificate info from JKS format file.
# 
def get_jks_days_to_expire(cert_info):
    cert_expire_data = {}
    for path in glob.glob(cert_info['path']):
        alias_expire_data = {}
        keystore = jks.KeyStore.load(path, cert_info['passphrase'])
        for cn, pk in keystore.private_keys.items():
            if cn in constant.EXCLUDE_COMMON_NAME:
                continue
            pk_entry = keystore.private_keys[cn]
            x509 = OpenSSL.crypto.load_certificate(_ASN1, pk_entry.cert_chain[0][1])
            common_name = x509.get_subject().CN
            time_to_expire = datetime.datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ').strftime('%s')
            current_time = datetime.date.today().strftime('%s')
            days_left = int(time_to_expire) - int(current_time)
            alias_expire_data[common_name]=int(days_left/(60*60*24))
            print_msg(common_name,path, alias_expire_data[common_name])
        for cn, pk in keystore.certs.items():
            if cn in constant.EXCLUDE_COMMON_NAME:
                continue
            trust_entry = keystore.certs[cn]
            x509 = OpenSSL.crypto.load_certificate(_ASN1, trust_entry.cert)
            common_name = x509.get_subject().CN
            time_to_expire = datetime.datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ').strftime('%s')
            current_time = datetime.date.today().strftime('%s')
            days_left = int(time_to_expire) - int(current_time)
            alias_expire_data[common_name]=int(days_left/(60*60*24))
            print_msg(common_name,path, alias_expire_data[common_name])
        cert_expire_data[path] = alias_expire_data
    return cert_expire_data

#Get certificate info from PEM format file.
# 
def get_pem_days_to_expire(cert_info):
    cert_expire_data = {}
    for path in glob.glob(cert_info['path']):
        alias_expire_data = {}
        cert = open(path, 'rt').read()
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        common_name = x509.get_subject().CN
        time_to_expire = datetime.datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ').strftime('%s')
        current_time = datetime.date.today().strftime('%s')
        days_left = int(time_to_expire) - int(current_time)
        alias_expire_data[common_name]=int(days_left/(60*60*24))
        print_msg(common_name,path, int(days_left/(60*60*24)))
        cert_expire_data[path] = alias_expire_data
    return cert_expire_data 

#Get certificate info from PKCS format file.
# 
def get_pkcs_days_to_expire(cert_info):
    cert_expire_data = {}
    for path in glob.glob(cert_info['path']):
        alias_expire_data = {}
        x509 = crypto.load_pkcs12(open(path, 'rb').read(), bytes(cert_info['passphrase'], 'utf-8') )
        common_name = x509.get_certificate().get_subject().CN
        time_to_expire = datetime.datetime.strptime(x509.get_certificate().get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ').strftime('%s')
        current_time = datetime.date.today().strftime('%s')
        days_left = int(time_to_expire) - int(current_time)
        alias_expire_data[common_name]=int(days_left/(60*60*24))
        print_msg(common_name,path, int(days_left/(60*60*24)))
        cert_expire_data[path] = alias_expire_data
    return cert_expire_data 

#Get certificate info from P12 format file.
#
def get_p12_days_to_expire(cert_info):
    cert_expire_data = {}
    for path in glob.glob(cert_info['path']):
        alias_expire_data = {}
        x509 = crypto.load_pkcs12(open(path, 'rb').read(), cert_info['passphrase'])
        common_name = x509.get_certificate().get_subject().CN
        time_to_expire = datetime.datetime.strptime(x509.get_certificate().get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ').strftime('%s')
        current_time = datetime.date.today().strftime('%s')
        days_left = int(time_to_expire) - int(current_time)
        alias_expire_data[common_name]=int(days_left/(60*60*24))
        print_msg(common_name,path, int(days_left/(60*60*24)))
        cert_expire_data[path] = alias_expire_data
    return cert_expire_data

