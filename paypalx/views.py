## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

import logging

from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.http import HttpResponseNotFound
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.utils.timezone import now

from models import Transaction
from paypalx import lib

log = logging.getLogger(__name__)

def init(req):
    """
    Init payment and redirect to robokassa site for checkout

    Required params:
    * amount - Amount to pay
    * [currency] - Currency code
    """

    data = req.GET

    amount = data.get("amount", None)
    description = data.get("description", "Test payment")
    currency = data.get("description", lib.conf("PPX_DEFAULT_CURRENCY"))

    if None in (amount, description):
        return HttpResponseBadRequest()

    try:
        tr = Transaction(amount=amount,
                         currency=currency,
                         description=description)
        tr.save()

        return_url = lib.conf("PPX_RETURN_URL")
        cancel_url = lib.conf("PPX_CANCEL_URL")

        params = {
            "METHOD": "SetExpressCheckout",
            "VERSION": lib.conf("PPX_VERSION"),
            "USER": lib.conf("PPX_USER"),
            "PWD": lib.conf("PPX_PWD"),
            "SIGNATURE": lib.conf("PPX_SIGNATURE"),
            "PAYMENTREQUEST_0_AMT": amount,
            "PAYMENTREQUEST_0_CURRENCYCODE": currency,
            "RETURNURL": return_url,
            "CANCELURL": cancel_url,
            "PAYMENTREQUEST_0_PAYMENTACTION": lib.conf("PPX_PAYMENT_ACTION"),
            }

        result = lib.call_api(params)

        if result.get("ACK", None) != "Success":
            raise Exception("Response ACK is not Success: %s" % result)

        if result.get("TOKEN", None) is None:
            raise Exception("No TOKEN in response: %s" % result)
        else:
            token = result["TOKEN"]

            tr.token = token
            tr.date_after_set = now()
            tr.set_ec_correlation_id = result.get("CORRELATIONID", "EMPTY")
            tr.save()

        return redirect(lib.get_paypal_url(token))
    except Exception as e:
        log.error("Unable to init transaction: %s", e)

        return HttpResponseServerError()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def return_url(req):
    token = req.GET.get("token", None)
    payer_id = req.GET.get("PayerID", None)

    try:
        if token is None:
            raise Exception("Token param not specified")

        if payer_id is None:
            raise Exception("PayerID param not specified")

        # Try to find transaction
        tr = Transaction.objects.get(token=token)

        if tr.completed:
            raise Exception("Transaction %d already completed: %s",
                            tr.id, tr.date_completed)

        # Obtain transaction details from paypal
        params = {
            "METHOD": "GetExpressCheckoutDetails",
            "VERSION": lib.conf("PPX_VERSION"),
            "USER": lib.conf("PPX_USER"),
            "PWD": lib.conf("PPX_PWD"),
            "SIGNATURE": lib.conf("PPX_SIGNATURE"),
            "TOKEN": token,
            }

        result = lib.call_api(params)

        if result.get("ACK") != "Success":
            raise Exception("Response ACK is not Success: %s" % str(result))

        # Save addition buyer info
        tr.payer_id = payer_id
        tr.buyer_email = result.get("EMAIL", "")
        tr.buyer_country = result.get("COUNTRYCODE", "")
        tr.buyer_first_name = result.get("FIRSTNAME", "")
        tr.buyer_last_name = result.get("LASTNAME", "")
        tr.save()

        # Do payment
        params = {
            "METHOD": "DoExpressCheckoutPayment",
            "VERSION": lib.conf("PPX_VERSION"),
            "USER": lib.conf("PPX_USER"),
            "PWD": lib.conf("PPX_PWD"),
            "SIGNATURE": lib.conf("PPX_SIGNATURE"),
            "TOKEN": token,
            "PAYERID": payer_id,
            "PAYMENTREQUEST_0_AMT": tr.amount,
            "PAYMENTREQUEST_0_CURRENCYCODE": tr.currency,
            "PAYMENTREQUEST_0_PAYMENTACTION": lib.conf("PPX_PAYMENT_ACTION"),
            }

        result = lib.call_api(params)

        if result.get("ACK") != "Success":
            raise Exception("Response ACK is not Success: %s" % str(result))

        tr.do_ec_correlation_id = result.get("CORRELATIONID", "EMPTY")
        tr.date_paid = now()
        tr.completed = True
        tr.save()

        return HttpResponse()
    except Transaction.DoesNotExist:
        log.error("Unable to find transaction with token %s", token)

        return HttpResponseNotFound()
    except Exception as e:
        log.error("Error (token=%s): %s", token, e)

        return HttpResponseServerError()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def cancel_url(req):
    token = req.GET.get("token", None)

    return HttpResponse()
