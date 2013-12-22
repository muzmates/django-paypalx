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

def init(amount, description=None, currency=None, req=None):
    """
    Init payment

    Params:
    * amount - Amount to pay
    * description - Transaction description
    * currency - Currency code
    * req - Original HttpRequest instance

    Return paypalx.models.Transaction instance
    """

    description = description or lib.dyn_conf("PPX_DEFAULT_DESCRIPTION", req)
    currency = currency or lib.dyn_conf("PPX_DEFAULT_CURRENCY", req)

    tr = models.Transaction(amount=Decimal(amount),
                            currency=currency,
                            description=description)

    params = {
        "METHOD": "SetExpressCheckout",
        "VERSION": lib.dyn_conf("PPX_VERSION", req),
        "USER": lib.dyn_conf("PPX_USER", req),
        "PWD": lib.dyn_conf("PPX_PWD", req),
        "SIGNATURE": lib.dyn_conf("PPX_SIGNATURE", req),
        "PAYMENTREQUEST_0_AMT": amount,
        "PAYMENTREQUEST_0_ITEMAMT": amount,
        "PAYMENTREQUEST_0_CURRENCYCODE": currency,
        "RETURNURL": lib.dyn_conf("PPX_RETURN_URL", req),
        "CANCELURL": lib.dyn_conf("PPX_CANCEL_URL", req),
        "L_PAYMENTREQUEST_0_NAME0": description,
        "L_PAYMENTREQUEST_0_QTY0": 1,
        "L_PAYMENTREQUEST_0_AMT0": amount,
        "PAYMENTREQUEST_0_PAYMENTACTION": lib.dyn_conf("PPX_PAYMENT_ACTION", req)
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

