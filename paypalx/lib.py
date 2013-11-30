## coding=utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

import urllib

from django.conf import settings

from paypalx import defaults

__all__ = ["conf",
           "get_endpoint",
           "get_paypal_url",
           "call_api"
           ]

def conf(val):
    """
    Get configuration param
    """

    return getattr(settings, val, getattr(defaults, val))

def get_endpoint():
    """
    Get paypal endpoint
    """

    return conf("PPX_SANDBOX_ENDPOINT") if conf("PPX_USE_SANDBOX") \
                                        else conf("PPX_ENDPOINT")

def get_paypal_url(token):
    """
    Get paypal redirect url
    """

    if conf("PPX_USE_SANDBOX"):
        base = conf("PPX_SANDBOX_REDIRECT_URL")
    else:
        base = conf("PPX_REDIRECT_URL")

    return base % urllib.urlencode({"token": token, "useraction": "commit"})

def call_api(data):
    """
    Make API call
    """

    import urllib2
    import urlparse
    from contextlib import closing
    from https_connection import build_opener

    opener = build_opener()
    req = urllib2.Request(get_endpoint(), urllib.urlencode(data))

    with closing(opener.open(req)) as stream:
        return dict(urlparse.parse_qsl(stream.read()))

def get_transaction_details(token):
    """
    Get transaction details by token
    """

    params = {
        "METHOD": "GetExpressCheckoutDetails",
        "VERSION": conf("PPX_VERSION"),
        "USER": conf("PPX_USER"),
        "PWD": conf("PPX_PWD"),
        "SIGNATURE": conf("PPX_SIGNATURE"),
        "TOKEN": token
    }

    return call_api(params)
