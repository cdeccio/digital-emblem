from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import AttributeOID, NameOID

from pathlib import Path
from random import randint

import pdb# debugging
import ipaddress


CURRENT_APPROVER_PATH = Path('current_approver.txt')
try:
    approver_domain = CURRENT_APPROVER_PATH.read_text().strip()
except FileNotFoundError:
    approver_domain = ''
app_host = 'localhost'
app_port = 5112

approved_requestors = ['rescue.icrc-external.jhuapl.org',
                        'myapp.ifrc.jhuapl.org']

crypto_root = Path('crypto')
req_root = Path('requestor_artifacts')##TODO:replace references to this w/cert_params.requester_root in tlsarecord.py and any other places this value is used

# def is_port_free(host: str, port: int) -> bool:
#     import socket
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         return s.connect_ex((host, port)) != 0

# def get_available_port(host: str) -> int:
#     while True:
#         port = randint(9000, 32000)
#         if is_port_free(app_host, port):
#             break
#     return port

# app_port = get_available_port(app_host)



class cert_params():
    #public_key
    #subject_name
    #basic_constraints
    #port
    #protocol
    #req_root
    #approver
    #approver_path 
    ##jhuapl = "jhuapl.org"
    #cert_dir
    ##crypto_root = Path(f'{certDir.name}/crypto')
    #subj_alt_names

    #x509 name object specifically intended for the subjectName field
    def create_name_obj(self,commonName,countryName,stateProvName,localeName,orgName):
       return x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, commonName),
        x509.NameAttribute(NameOID.COUNTRY_NAME, countryName),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, stateProvName),
        x509.NameAttribute(NameOID.LOCALITY_NAME, localeName),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, orgName),
    ])
 

    def __get_secret_key_pem__(self):
        secret_key_pem = self.__secret_key__.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=NoEncryption())
        return secret_key_pem


    def write_secret_key_pem(self,filePath):
        pemVal = self.__get_secret_key_pem__()
        filePath.write_bytes(pemVal)

    def __set_subject_name__(self,commonName,countryName,stateProvName,localeName,orgName):
        self.subject_name = self.create_name_obj(commonName,countryName,stateProvName,localeName,orgName)  


    def __set_basic_constraints__(self,isCA,pathLen=0):
        self.basic_constraints = x509.BasicConstraints(ca=isCA, path_length=pathLen)


    def set_approver_domain(self):
        try:
            self.approver_domain = self.approver_path.read_text().strip()
        except FileNotFoundError:
            self.approver_domain = ''

    #Base __init__ with default/placeholder parameter values
    def __init__(self,pathLen=0,port=443,protocol='tcp',approver='icrc'):
       self.__init__(f'_{self.port}._{self.protocol}.{self.counter}.rescue.icrc-external.jhuapl.org',
                     u"US",u"District of Columbia",u"Washington",u"ICRC-external",False)


    #Overload to allow additional values to be passed in.
    def __init__(self,commonName,countryName,stateProvName,localeName,orgName,isCA,pathLen=0,port=443,protocol='tcp',approver='icrc'):
        self._set_subject_name_(commonName,countryName,stateProvName,localeName,orgName)
        self.__secret_key__ = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend())
        self.public_key = self.__secret_key__.public_key()
        self.cert_dir = Path('cert-path')
        #crypto_root = Path(f'{certDir.name}/crypto')
        self.req_root = Path(f'{self.cert_dir.name}/requestor_artifacts')
        self.approver = approver
        self.approver_path = Path(f'{self.cert_dir.name}/current_approver.txt')
        self.approver_domain=''



##########################################################
# End Entity Certificate request parameters and functions #
##########################################################
class ee_cert_params(cert_params):
    
    
    def __initialize__(self,commonName,countryName,stateProvName,localeName,orgName,port=443,protocol='tcp',certDirName='ee-cert',approver=None):
        self.__secret_key__ =rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()) 
        self.public_key = self.__secret_key__.public_key()
        self.cert_dir = Path(certDirName)
        self.name=super().create_name_obj(commonName,countryName,stateProvName,localeName,orgName)
        # pdb.set_trace()
        self.basic_constraints = x509.BasicConstraints(ca=False, path_length=None)
        self.req_root = Path(f'{self.cert_dir.name}/requestor_artifacts')
        self.approver_path = Path(f'{self.cert_dir.name}/current_approver.txt')
        
        #initialize empty x509 extension fields
        self.subj_alt_names=None
        self.subj_key_identifier = x509.SubjectKeyIdentifier.from_public_key(self.public_key)
        self.cert_policies = None


    def __init__(self,port=443,protocol='tcp',counterFile=Path('ee-cert/counter.txt')):
        try:
            # Try to load the counter from the existing file
            counter = int(counterFile.read_text())
        except FileNotFoundError:
            # If the file doesn't exist, initialize the counter to 0
            counter = 0
        commonName = f'_{port}._{protocol}.{counter}.rescue.icrc-external.jhuapl.org'
        self.__initialize__(commonName,u"US",u"District of Columbia",u"Washington",u"ICRC-external")
        counter+=1
        counterFile.write_text(f'{counter}')



    def set_subject_alternative_name(self,domain,nameType):
        nameEntry=None
        if nameType is None or not isinstance(nameType,str) or nameType not in ['dnstype','rfc822Type','uriType','dirNameType', 'ipAddrType']:
            raise AttributeError(f'Unrecognized nameType {nameType}.\r' +
            'nameType must be one of the following strings:' + 
            '\'dnstype\',\'rfc822Type\',\'uriType\',\'dirNameType\' or \'ipAddrType\'')
        if nameType == 'ipAddrType':
            try:
                ipDomain = ipaddress.ip_network(domain)
                nameEntry = x509.IPAddress(ipDomain)
            except (TypeError,ipaddress.AddressValueError) as te:
                raise te.with_traceback()
        elif nameType=='dnsType':
            nameEntry = x509.DNSName(domain)
        elif nameType=='rfc822Type':
            nameEntry = x509.RFC822Name(domain)
        elif nameType=='dirNameType':
            if isinstance(domain,x509.Name):
                nameEntry = x509.DirectoryName(domain)
        else:
            if nameType=='uriType':
                nameEntry = x509.UniformResourceIdentifier(domain)

        #self.subj_alt_names gets initialized to None, so check for that case.
        if self.subj_alt_names is None:
            if nameEntry is None:
                raise TypeError(f'The certificate\'s \'subjectName\' attribute and its \'subjectAlternativeName\' cannot both be None.'  )
            self.subj_alt_names = x509.SubjectAlternativeName([nameEntry])
        else:
            if not isinstance(self.subj_alt_names.get_values_for_type(x509.GeneralName),list):
                raise RuntimeError()
            if nameEntry is not None:
                self.subj_alt_names = x509.SubjectAlternativeName(self.subj_alt_names.get_values_for_type(x509.GeneralName).append(nameEntry))
        return
    


    def write_secret_key_pem(self,filePath):
        super().write_secret_key_pem(filePath)



    def sign_csr_builder(self,builder):
        return builder.sign(self.__secret_key__, hashes.SHA256(), default_backend())



    # CertificatePolicies
    #********************
    #placeholder functions for initializing certificate policies (self.cert_policies)
    #These would be fleshed out in the case we decide to require a specific set of certificate policies and identifiers 
    # to denote that the signed EE cert is a digital emblem.

    #TODO: revisit these functions if/when you've defined certificate policies for the CA cert(s) - mechanism for constructing these will likely need to be fixed/rebuilt   

    # Note that the policyID parameter would likely be hard-coded to a default value or would be a chosen value from a predefined list of OIDs.
    def __set_base_policy_info__(policyID,explicitTextVal = None):
        if explicitTextVal is None or explicitTextVal=='':
            explicitTextVal = 'Digital Emblem' 
        basePolicyQual = x509.UserNotice(None,explicitTextVal)#TODO:Discuss whether to use certificatePolicies to denote a DE and if so, the text fields it would need to require
        
        #placeholder/base case - still need to determine which policy qualifiers would be required if any
        policyQualifiers = [basePolicyQual]
        return x509.PolicyInformation(policyID,policyQualifiers)


    #build up list of policies into an iterable of x509.PolicyInformation objects
    # oids is either a dict of form {idVal:explicitText} or a list of tuples of form (idVal,explicitText)
    # where idVal is an x509.ObjectIdentifier and explicitText is a string 
    def __build_policy_list__(self,oids):
        return [self.__set_base_policy_info__(idVal,explicitText) for idVal,explicitText in oids]    

    

    def __check_policyListSpecs__(policyListSpecs):
        return all([isinstance(policy,x509.PolicyInformation) for policy in policyListSpecs])


    def set_cert_policies(self,policyListSpecs):
        if self.__check_policyListSpecs__(policyListSpecs):
            self.cert_policies = x509.CertificatePolicies(policyListSpecs)
        else:
            policyList = self.__build_policy_list__(policyListSpecs)
            self.cert_policies = x509.CertificatePolicies(policyList)
    #  
    #***************   
        

    #determine which extension fields to set and initialize them
    def set_extension_fields(self):
        pass#placeholder


###############################################################
#Cert. Authority Certificate request parameters and functions #
###############################################################

class ca_cert_params(cert_params):

    def __initialize__(self,commonName,countryName,stateProvName,localeName,orgName,port=443,protocol='tcp',certDirName='ca-cert',approver=None):
        self.__secret_key__ =rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend())
        self.public_key = self.__secret_key__.public_key()
        self.cert_dir = Path(certDirName)
        self.name=super().create_name_obj(commonName,countryName,stateProvName,localeName,orgName)
        self.basic_constraints = x509.BasicConstraints(ca=True, path_length=0)
        self.req_root = Path(f'{self.cert_dir.name}/requestor_artifacts')
        self.approver_path = Path(f'{self.cert_dir.name}/current_approver.txt')
        self.subj_alt_names=None
        self.subj_key_identifier = x509.SubjectKeyIdentifier.from_public_key(self.public_key)
        self.cert_policies = None


    
    def __init__(self,approver_path=CURRENT_APPROVER_PATH,selfSigned=True,approver=None,port=443,protocol='tcp',certDirName='ca-cert'):
        if selfSigned:
            pass#placeholder
        if approver is None or not isinstance(str,approver):
            self.approver ='icrc' 
        else:
            self.approver = approver
        self.approver_path = approver_path
        try:
            self.approver_domain = self.approver_path.read_text().strip()
        except FileNotFoundError:
            self.approver_domain = ''
        counterFile = Path(f'{certDirName}/counter.txt')
        try:
            # Try to load the counter from the existing file
            counter = int(counterFile.read_text())
        except FileNotFoundError:
            # If the file doesn't exist, initialize the counter to 0
            counter = 0
        commonName = f'_{port}._{protocol}.{counter}.{self.approver}.jhuapl.org'
        self.__initialize__(commonName,u"US",u"Maryland",u"Laurel",u"ICRC")
        counter+=1
        counterFile.write_text(f'{counter}')
    

    def set_subject_alternative_name(self,domain,nameType):
        nameEntry=None
        if nameType is None or not isinstance(nameType,str) or nameType not in ['dnstype','rfc822Type','uriType','dirNameType', 'ipAddrType']:
            raise AttributeError(f'Unrecognized nameType {nameType}.\r' +
            'nameType must be one of the following strings:' +
            '\'dnstype\',\'rfc822Type\',\'uriType\',\'dirNameType\' or \'ipAddrType\'')
        if nameType == 'ipAddrType':
            try:
                ipDomain = ipaddress.ip_network(domain)
                nameEntry = x509.IPAddress(ipDomain)
            except (TypeError,ipaddress.AddressValueError) as te:
                raise te.with_traceback()
        elif nameType=='dnsType':
            nameEntry = x509.DNSName(domain)
        elif nameType=='rfc822Type':
            nameEntry = x509.RFC822Name(domain)
        elif nameType=='dirNameType':
            if isinstance(domain,x509.Name):
                nameEntry = x509.DirectoryName(domain)
        else:
            if nameType=='uriType':
                nameEntry = x509.UniformResourceIdentifier(domain)

        #self.subj_alt_names gets initialized to None, so check for that case.
        if self.subj_alt_names is None:
            if nameEntry is None:
                raise TypeError(f'The certificate\'s \'subjectName\' attribute and its \'subjectAlternativeName\' cannot both be None.'  )
            self.subj_alt_names = x509.SubjectAlternativeName([nameEntry])
        else:
            if not isinstance(self.subj_alt_names.get_values_for_type(x509.GeneralName),list):
                raise RuntimeError()
            if nameEntry is not None:
                self.subj_alt_names = x509.SubjectAlternativeName(self.subj_alt_names.get_values_for_type(x509.GeneralName).append(nameEntry))
        return




    def write_secret_key_pem(self,filePath):
        super().write_secret_key_pem(filePath)


    def sign_cert_builder(self,builder):
        return builder.sign(self.__secret_key__, hashes.SHA256(), default_backend())
