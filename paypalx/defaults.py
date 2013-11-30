## coding=utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from django.http import HttpResponseServerError, HttpResponse

## User overridable settings
PPX_VERSION = "93"
PPX_USER = ""
PPX_PWD = ""
PPX_SIGNATURE = ""
PPX_DEFAULT_CURRENCY = "USD"
PPX_DEFAULT_DESCRIPTION = "Payment"
PPX_RETURN_URL = ""
PPX_CANCEL_URL = ""
PPX_PAYMENT_ACTION = "Sale"
PPX_USE_SANDBOX = False
PPX_RETURN_URL_SUCCESS_CALLBACK = lambda req, tr: HttpResponse()
PPX_RETURN_URL_ERROR_CALLBACK = lambda req, tr, err: HttpResponseServerError()
PPX_CANCEL_URL_CALLBACK = lambda req, tr: HttpResponse()
PPX_SSL_CA_CERT_PATH = "/etc/ssl/certs/ca-certificates.crt"

## Usually you don't need to override these
PPX_ENDPOINT = "https://api-3t.paypal.com/nvp"
PPX_SANDBOX_ENDPOINT = "https://api-3t.sandbox.paypal.com/nvp"

PPX_SANDBOX_REDIRECT_URL = "https://www.sandbox.paypal.com/webscr?cmd=_express-checkout&%s"
PPX_REDIRECT_URL = "https://www.paypal.com/webscr?cmd=_express-checkout&%s"
