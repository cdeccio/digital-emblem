#!/usr/bin/python3

import unittest

import mock
import json


from certbot import errors
from certbot.compat import os
from certbot.plugins import dns_test_common
from certbot.plugins.dns_test_common import DOMAIN
from certbot.tests import util as test_util



class AuthenticatorTest(
        test_util.TempDirTestCase, dns_test_common.BaseAuthenticatorTest
    ):
    def setUp(self):
        super(AuthenticatorTest, self).setUp()

        from certbot-dns-tsig.dns01_tsig import Authenticator
