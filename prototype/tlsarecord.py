#!/usr/bin/env python3

import binascii
from datetime import datetime, timedelta, timezone
from common import crypto_root, CURRENT_APPROVER_PATH,ee_cert_params,ca_cert_params
#from default_params.ee_params import #TODO: define params and add them here
from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption
from pathlib import Path
import random
import plac

# src: https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
# src: https:https://cryptography.io/en/3.4.6/hazmat/primitives/asymmetric/html

#TODO: Create default param files for CA and EE.
# Move relevant fields to the respective files. If the field value will be consistent for both specify it in common.py
# host_information
port = 443
protocol = 'tcp'
approver = 'icrc'
jhuapl = "jhuapl.org"


def generate_x509(certParams, current, extensionFields):
    serial = random.randint(1, 2**32-1)
    builder = x509.CertificateBuilder() \
                   .subject_name(certParams.name) \
                   .issuer_name(certParams.name) \
                   .public_key(certParams.public_key) \
                   .serial_number(serial) \
                   .not_valid_before(current) \
                   .not_valid_after(current + timedelta(days=365))
    criticalityDict = {
        'basic_constraints':True,
        'subj_alt_names':certParams.name is None or certParams.name=='',
        'subj_key_identifier':False,
        'cert_policies':False
        }
    for field in extensionFields:
        builder = add_csr_extension(builder,field,criticalityDict)
    return certParams.sign_cert_builder(builder)

def get_cert_hex(certificate):
    # Gets the DER-encoded certificate data
    certificate_data = certificate.public_bytes(Encoding.DER)

    # Converts the DER-encoded data to hexadecimal to put into TLSA record
    certificate_hex = binascii.hexlify(certificate_data).decode('utf-8')

    return certificate_hex


# Encoding code and certificate
def get_cert_pem(certificate):
    cert_pem = certificate.public_bytes(encoding=Encoding.PEM)
    return cert_pem


def get_private_key_pem(private_key):
    private_key_pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=NoEncryption())
    return private_key_pem


def get_public_key_pem(pub_key):
    public_key_pem = pub_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo
    )
    return public_key_pem



def add_csr_extension(csrBuilder,fields,criticalityDict):
    fieldName,fieldVal = fields
    if fieldVal is None and criticalityDict[fieldName]:
        raise AttributeError(f'The {fieldName} extension field was marked as critical, but set to None.'+
        '\r x509 extensions marked as critical must be explicitly set to a meaningful value.')
    elif fieldVal is not None:
        return csrBuilder.add_extension(fieldVal,criticalityDict[fieldName])
    return csrBuilder


def generate_x509_csr(certParams,extensionFields):
    builder = x509.CertificateSigningRequestBuilder() \
        .subject_name(certParams.name) 

    # Whether each extension is critical.
    # Per RFC 5280 whether or not the certificatePolicy (cert_policies) extension is marked as critical is determined by the application
    # i.e. whether the signing CA/application specifies which policies (identified by policy OID ) it will accept. (See RFC 5280 §4.2.1.4.)
    criticalityDict = {
        'basic_constraints':True,
        'subj_alt_names':certParams.name is None or certParams.name=='',
        'subj_key_identifier':False,
        'cert_policies':False
        }
    for field in extensionFields:
        builder = add_csr_extension(builder,field,criticalityDict) 
    return certParams.sign_csr_builder(builder)





# TODO:Generalize to allow function/script to be called to generate an EE cert and to generate a CA cert
#     Also enable addition of specific x.509 extension fields for the sake of easier experimenting. (RF)
@plac.pos('isCA', help='(Boolean) whether to generate a CA certificate', type=bool)
@plac.pos('subjAltNames', help="dict containing all subjectAlternativeNames to include in the cert (keys) and their respective name-type ('dnstype','rfc822Type','uriType','dirNameType' or 'ipAddrType')")
def main(isCA=False,subjAltNames=dict()):
    f_counter = Path('counter.txt')#None# 
    certParams = None
    #TODO: Review logic for CA case. Make sure the code there actually works as expected
    if isCA:
        certParams = ca_cert_params()
        f_counter = Path(f'{certParams.cert_dir.name}/counter.txt')#TODO: use a parameter file to determine the filepath for the [root] CA cert 
        
        current = datetime.now(timezone.utc)

        for altName,nameType in subjAltNames.items():
            certParams.set_subject_alternative_name(altName,nameType)
        #TODO: Fix this call to account for encapsulization of the secret_key
        extFields = {
            'basic_constraints':certParams.basic_constraints,
            'subj_alt_names':certParams.subj_alt_names,
            'subj_key_identifier':certParams.subj_key_identifier,
            'cert_policies':certParams.cert_policies
            }
        certificate = generate_x509(certParams, current, extFields.items())
        cert_hex = get_cert_hex(certificate)
        print("Certificate hex:", cert_hex)
        #cert_params.approver_path.write_text(approver_domain)
        plaintext_name = certParams.name.rdns[0].rfc4514_string()[3:]
        CURRENT_APPROVER_PATH.write_text(plaintext_name)
        (crypto_root/f'{plaintext_name}_cert.pem').write_bytes(get_cert_pem(certificate))
        certParams.write_secret_key_pem(crypto_root/f'{plaintext_name}_priv.key.pem')
        (crypto_root/f'{plaintext_name}_pub.key.pem').write_bytes(get_public_key_pem(certParams.public_key))
        (crypto_root/f'{plaintext_name}_cert.hex').write_text(cert_hex)
    else:
        certParams = ee_cert_params()
        f_counter = Path(f'{certParams.cert_dir.name}/counter.txt')

        #Set the extensions that will be used for the DE EE cert.
        for altName,nameType in subjAltNames.items():
            certParams.set_subject_alternative_name(altName,nameType)
        extFields = {
            'basic_constraints':certParams.basic_constraints,
            'subj_alt_names':certParams.subj_alt_names,
            'subj_key_identifier':certParams.subj_key_identifier,
            'cert_policies':certParams.cert_policies
            }
        eeCSR = generate_x509_csr(certParams,extFields.items())
        csrHex = get_cert_hex(eeCSR)
        print('CSR hex:', csrHex)
        plaintext_name = certParams.name.rdns[0].rfc4514_string()[3:]
        (crypto_root/f'{plaintext_name}_csr.pem').write_bytes(get_cert_pem(eeCSR))
        certParams.write_secret_key_pem(crypto_root/f'{plaintext_name}_priv.key.pem')
        (crypto_root/f'{plaintext_name}_pub.key.pem').write_bytes(get_public_key_pem(certParams.public_key))
        (crypto_root/f'{plaintext_name}_csr.hex').write_text(csrHex)

if __name__ == "__main__":
	plac.call(main)
