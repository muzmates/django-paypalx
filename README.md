# Overview

django-paypalx is a django application for integrating paypal
express checkout payments.

# Module settings

```python
PPX_VERSION = "XX.0"
PPX_USER = ""
PPX_PWD = ""
PPX_SIGNATURE = ""
PPX_DEFAULT_CURRENCY = "USD"
PPX_RETURN_URL = ""
PPX_CANCEL_URL = ""
PPX_PAYMENT_ACTION = "Sale"
PPX_USE_SANDBOX = False
PPX_SSL_CA_CERT_PATH = "/etc/ssl/certs/ca-certificates.crt"
```

# Installation

1. Add `paypalx` application to your `INSTALLED_APPS`

2. Add following to your main urls.py:

```python
    url('ppx/', include('paypalx.urls')),
```

3. Run manage.py syncdb && manage.py migrate paypalx

# Callback function

function()
