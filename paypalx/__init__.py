## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from decimal import Decimal

from django.utils.timezone import now

import lib
import models
import ex

def init(amount, description=None, currency=None):
    """
    Init payment and redirect to robokassa site for checkout

    Params:
    * amount - Amount to pay
    * description - Transaction description
    * currency - Currency code

    Return paypalx.models.Transaction instance
    """

    description = description or lib.conf("PPX_DEFAULT_DESCRIPTION")
    currency = currency or lib.conf("PPX_DEFAULT_CURRENCY")

    tr = models.Transaction(amount=Decimal(amount),
                            currency=currency,
                            description=description)

    return_url = lib.conf("PPX_RETURN_URL")
    cancel_url = lib.conf("PPX_CANCEL_URL")

    params = {
        "METHOD": "SetExpressCheckout",
        "VERSION": lib.conf("PPX_VERSION"),
        "USER": lib.conf("PPX_USER"),
        "PWD": lib.conf("PPX_PWD"),
        "SIGNATURE": lib.conf("PPX_SIGNATURE"),
        "PAYMENTREQUEST_0_AMT": amount,
        "PAYMENTREQUEST_0_ITEMAMT": amount,
        "PAYMENTREQUEST_0_CURRENCYCODE": currency,
        "RETURNURL": return_url,
        "CANCELURL": cancel_url,
        "L_PAYMENTREQUEST_0_NAME0": description,
        "L_PAYMENTREQUEST_0_QTY0": 1,
        "L_PAYMENTREQUEST_0_AMT0": amount,
        "PAYMENTREQUEST_0_PAYMENTACTION": lib.conf("PPX_PAYMENT_ACTION"),
        }

    result = lib.call_api(params)

    if result.get("ACK", None) != "Success":
        raise ex.ResponseNotSuccess(result)

    if result.get("TOKEN", None) is None:
        raise ex.ResponseMissingData("TOKEN")
    else:
        token = result["TOKEN"]

    tr.token = token
    tr.date_after_set = now()
    tr.set_ec_correlation_id = result.get("CORRELATIONID", "EMPTY")

    tr.save()

    return tr
