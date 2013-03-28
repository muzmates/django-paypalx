## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

import decimal
import mock

from django.test import TestCase

import paypalx

#from django.utils.timezone import now
#from django.core.urlresolvers import reverse
#from django.contrib.auth.models import User

SETTINGS = {"PPX_USER": "",
            "PPX_PWD": "",
            "PPX_SIGNATURE": "",
            "PPX_DEFAULT_CURRENCY": "USD",
            "PPX_RETURN_URL": "",
            "PPX_CANCEL_URL": "",
            "PPX_USE_SANDBOX": True}

def mconf(val):
    return SETTINGS.get(val)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestInit(TestCase):
    @mock.patch('paypalx.lib.conf', mconf)
    def test_correct_init(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @mock.patch('paypalx.lib.conf', mconf)
    @mock.patch('paypalx.lib.call_api', lambda _: {"ACK": "ERROR"})
    def test_set_ec_not_ack(self):
        self.assertRaises(Exception, paypalx.init, 1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def test_invalid_args(self):
        self.assertRaises(decimal.InvalidOperation,
                          paypalx.init, amount="wtf")
