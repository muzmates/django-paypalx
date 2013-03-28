## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

import decimal
import mock

from django.test import TestCase

import paypalx

SETTINGS = {"PPX_USER": "",
            "PPX_PWD": "",
            "PPX_SIGNATURE": "",
            "PPX_DEFAULT_CURRENCY": "USD",
            "PPX_DEFAULT_DESCRIPTION": "Fake payment",
            "PPX_RETURN_URL": "",
            "PPX_CANCEL_URL": "",
            "PPX_USE_SANDBOX": True}

def mconf(val):
    return SETTINGS.get(val)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestInit(TestCase):
    @mock.patch('paypalx.lib.conf', mconf)
    @mock.patch('paypalx.lib.call_api', lambda _: {"ACK": "Success",
                                                   "TOKEN": "MY_TOKEN"})
    def test_correct_init(self):
        tr = paypalx.init(1)

        self.assertIsInstance(tr, paypalx.models.Transaction)
        self.assertEqual("MY_TOKEN", tr.token)
        self.assertIsNotNone(tr.date_after_set)
        self.assertIsNotNone(tr.set_ec_correlation_id)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @mock.patch('paypalx.lib.conf', mconf)
    @mock.patch('paypalx.lib.call_api', lambda _: {"ACK": "ERROR"})
    def test_set_ec_not_ack(self):
        self.assertRaises(Exception, paypalx.init, 1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @mock.patch('paypalx.lib.conf', mconf)
    @mock.patch('paypalx.lib.call_api', lambda _: {"ACK": "Success"})
    def test_set_ec_no_token(self):
        self.assertRaises(Exception, paypalx.init, 1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def test_invalid_args(self):
        self.assertRaises(decimal.InvalidOperation,
                          paypalx.init, amount="wtf")
