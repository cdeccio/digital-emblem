#!/usr/bin/python3


import re
import socket
import sys

import dns.name 
import dns.query
import dns.rcode
import dns.rdatatype
import dns.tsigkeyring
import dns.update 

from certbot import errors, interfaces
from certbot.plugins import dns_common

class Authenticator(dns_common.DNSAuthenticator):

    #WHERE YOU LEFT OFF (10/10/2024): Need to see about cleaning/overloading init <3 Past self
    def __init__(self,*args,**kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)#placeholder for now
        self.tsig_alg=None
        self.tsig_keyring=None
        #TODO: Check the functionality you need here

    
    # Adds plugin arguments to the CLI argument parser 
    # (see https://eff-certbot.readthedocs.io/en/latest/api/certbot.plugins.common.html#certbot.plugins.common.Plugin.add_parser_arguments)
    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator,cls).add_parser_arguments(add)

    
    #TODO
    #Placeholders for inherited functions that need to be implemented
    def auth_hint():
        pass


    #TODO
    # def get_chall_pref():
    #     pass


    #TODO
    # def prepare():
    #     pass
    

    #TODO
    # def more_info():
    #     pass
    


     
    def parse_tsig_key_file(self,file,TSIG_KEY_RE=None,TSIG_ALG_RE=None,TSIG_SECRET_RE=None):
        tsig_key = None
        secret = None
        # self.tsig_alg = None

        if TSIG_KEY_RE is None:
            TSIG_KEY_RE = re.compile(r'key\s+"([^"]+)"')
        if TSIG_ALG_RE is None:
            TSIG_ALG_RE = re.compile(r'algorithm\s+([^;\s]+)')
        if TSIG_SECRET_RE is None:
            TSIG_SECRET_RE = re.compile(r'secret\s+"([^"]+)"')

        for line in file:
            line = line.strip()
            kMsg = TSIG_KEY_RE.search(line)
            if kMsg is not None:
                tsig_key = kMsg.group(1)
            algMsg = TSIG_ALG_RE.search(line)
            if algMsg is not None:
                self.alg = algMsg.group(1)
            secMsg = TSIG_SECRET_RE.search(line)
            if secMsg is not None:
                secret = secMsg.group(1)
        self.tsig_keyring = dns.tsigkeyring.from_text({ tsig_key: secret })



    #TODO
    def perform():
        pass


    #TODO
    def cleanup():
        pass


