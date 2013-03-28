## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.http import HttpResponseNotFound
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.utils.timezone import now

import lib
from models import Transaction

def return_url(req):
    token = req.GET.get("token", None)
    payer_id = req.GET.get("PayerID", None)

    successf = lib.conf("PPX_RETURN_URL_SUCCESS_CALLBACK")
    failuref = lib.conf("PPX_RETURN_URL_ERROR_CALLBACK")

    tr = None

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
        result = lib.get_transaction_details(token)

        if result.get("ACK") != "Success":
            raise Exception("Response ACK is not Success: %s", str(result))

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
            "L_PAYMENTREQUEST_0_NAME0": tr.description,
            "L_PAYMENTREQUEST_0_QTY0": 1,
            "L_PAYMENTREQUEST_0_AMT0": tr.amount,
            }

        result = lib.call_api(params)

        if result.get("ACK") != "Success":
            raise Exception("Response ACK is not Success: %s", str(result))

        tr.do_ec_correlation_id = result.get("CORRELATIONID", "EMPTY")
        tr.date_paid = now()
        tr.completed = True
        tr.save()

        return successf(req, tr)
    except Transaction.DoesNotExist:
        e = Exception("Unable to find transaction with token %s", token)

        return failuref(req, tr, e)
    except Exception as e:
        return failuref(req, tr, e)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def cancel_url(req):
    token = req.GET.get("token", None)

    return HttpResponse()