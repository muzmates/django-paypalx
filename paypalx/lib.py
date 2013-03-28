## encoding: utf-8
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_endpoint():
    """
    Get paypal endpoint
    """

    return conf("PPX_SANDBOX_ENDPOINT") if settings.DEBUG \
                                        else conf("PPX_ENDPOINT")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_paypal_url(token):
    """
    Get paypal redirect url
    """

    if settings.DEBUG:
        base = conf("PPX_SANDBOX_REDIRECT_URL")
    else:
        base = conf("PPX_REDIRECT_URL")

    return base % urllib.urlencode({"token": token, "useraction": "commit"})

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def call_api(data):
    """
    Make API call
    """

    import urllib2
    import urlparse

    endpoint = get_endpoint()
    con = urllib2.urlopen(endpoint, urllib.urlencode(data))
    res = con.read()

    con.close()

    return dict(urlparse.parse_qsl(res))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
