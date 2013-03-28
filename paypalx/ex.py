## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

class PaypalxException(Exception):
    """
    Base exception
    """

    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ResponseNotSuccess(PaypalxException):
    """
    In API response ACK field is not Success

    Argument: response dict
    """

    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ResponseMissingData(PaypalxException):
    """
    Some data fields are missing in API response

    Argument: field name missing
    """

    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TransactionIsCompleted(PaypalxException):
    """
    Transaction is already completed

    Argument: Transaction instance
    """

    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TransactionNotFound(PaypalxException):
    """
    Transaction with provided token cannot be found in the database

    Argument: Provided token
    """

    pass
