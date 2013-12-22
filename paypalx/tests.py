## coding=utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

import decimal
import mock

from django.http import HttpResponseServerError, HttpResponse
from django.test import TestCase

import paypalx

from paypalx import views
from paypalx import ex

def err_cb(req, tr, e):
    raise e

SETTINGS = {"PPX_USER": "",
            "PPX_PWD": "",
            "PPX_SIGNATURE": "",
            "PPX_DEFAULT_CURRENCY": "USD",
            "PPX_DEFAULT_DESCRIPTION": "Fake payment",
            "PPX_RETURN_URL": "",
            "PPX_CANCEL_URL": "",
            "PPX_RETURN_URL_SUCCESS_CALLBACK": lambda req, tr: tr,
            "PPX_RETURN_URL_ERROR_CALLBACK": err_cb,
            "PPX_USE_SANDBOX": True}

def mconf(val):
    return SETTINGS.get(val)

class Reqx(object):
    def __init__(self, d):
        self.GET = d

@mock.patch('paypalx.lib.conf', mconf)
class TestInit(TestCase):
    @mock.patch('paypalx.lib.call_api', lambda _: {"ACK": "Success",
                                                   "TOKEN": "MY_TOKEN"})
    def test_correct_init(self):
        tr = paypalx.init(1)

        self.assertIsInstance(tr, paypalx.models.Transaction)
        self.assertEqual("MY_TOKEN", tr.token)
        self.assertIsNotNone(tr.date_after_set)
        self.assertIsNotNone(tr.set_ec_correlation_id)

    @mock.patch('paypalx.lib.call_api', lambda _: {"ACK": "ERROR"})
    def test_set_ec_not_success(self):
        self.assertRaises(ex.ResponseNotSuccess, paypalx.init, 1)

    @mock.patch('paypalx.lib.call_api', lambda _: {"ACK": "Success"})
    def test_set_ec_no_token(self):
        self.assertRaises(ex.ResponseMissingData, paypalx.init, 1)

    def test_invalid_args(self):
        self.assertRaises(decimal.InvalidOperation,
                          paypalx.init, amount="wtf")

@mock.patch('paypalx.lib.conf', mconf)
class TestReturn(TestCase):
    amount = 15
    token = "TEST_TOKEN"
    setup_data = {"ACK": "Success",
                  "TOKEN": token
                  }

    req_data = {"token": token,
                "PayerID": "id"
                }

    email = "test@gmail.com"
    country = "AF"
    first_name = "FIRST"
    last_name = "LAST"
    corr = "CORR"

    details = {"ACK": "Success",
               "EMAIL": email,
               "COUNTRYCODE": country,
               "FIRSTNAME": first_name,
               "LASTNAME": last_name
        }

    @mock.patch('paypalx.lib.call_api', lambda _: TestReturn.setup_data)
    def setUp(self):
        self.tr = paypalx.init(self.amount)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def test_no_token(self):
        self.assertRaises(ex.ResponseMissingData, views.return_url,
                          Reqx({}))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def test_no_payer_id(self):
        self.assertRaises(ex.ResponseMissingData, views.return_url,
                          Reqx({"token": ""}))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def test_invalid_token(self):
        self.assertRaises(ex.TransactionNotFound, views.return_url,
                          Reqx({"token": "wrong", "PayerID": "id"}))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def test_transaction_completed(self):
        self.tr.completed = True
        self.tr.save()

        self.assertRaises(ex.TransactionIsCompleted, views.return_url,
                          Reqx(self.req_data))

    @mock.patch('paypalx.lib.get_transaction_details', lambda _: {"ACK": "X"})
    def test_not_success(self):
        self.assertRaises(ex.ResponseNotSuccess, views.return_url,
                          Reqx(self.req_data))

    @mock.patch('paypalx.lib.get_transaction_details',
                lambda _: {"ACK": "Success"})
    @mock.patch('paypalx.lib.call_api', lambda _: {"ACK": "XXX"})
    def test_not_success2(self):
        self.assertRaises(ex.ResponseNotSuccess, views.return_url,
                          Reqx(self.req_data))

    @mock.patch('paypalx.lib.get_transaction_details',
                lambda _: TestReturn.details)
    @mock.patch('paypalx.lib.call_api',
                lambda _: {"ACK": "Success",
                           "CORRELATIONID": TestReturn.corr})
    def test_success(self):
        tr = views.return_url(Reqx(self.req_data))

        self.assertEqual(tr.buyer_email, self.email)
        self.assertEqual(tr.buyer_country, self.country)
        self.assertEqual(tr.buyer_first_name, self.first_name)
        self.assertEqual(tr.buyer_last_name, self.last_name)
        self.assertEqual(tr.do_ec_correlation_id, self.corr)
