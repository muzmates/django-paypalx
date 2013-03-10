## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

## User overridable settings
PPX_VERSION = "93"
PPX_USER = ""
PPX_PWD = ""
PPX_SIGNATURE = ""
PPX_DEFAULT_CURRENCY = "USD"
PPX_RETURN_URL = ""
PPX_CANCEL_URL = ""
PPX_PAYMENT_ACTION = "Sale"
PPX_USE_SANDBOX = False

## Usually you don't need to override these
PPX_ENDPOINT = "https://api-3t.paypal.com/nvp"
PPX_SANDBOX_ENDPOINT = "https://api-3t.sandbox.paypal.com/nvp"

PPX_SANDBOX_REDIRECT_URL = "https://www.sandbox.paypal.com/webscr?cmd=_express-checkout&%s"
PPX_REDIRECT_URL = "https://www.paypal.com/webscr?cmd=_express-checkout&%s"
