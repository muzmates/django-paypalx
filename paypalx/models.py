## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Transaction(models.Model):
    """
    Payment transactions
    """

    amount = models.DecimalField(max_digits=15, decimal_places=2,
                                 help_text=_("Payment amount"))

    description = models.TextField(max_length=100,
                                   help_text=_("Arbitrary payment notes"))

    currency = models.TextField(max_length=50,
                                help_text=_("Transaction currency"))

    token = models.CharField(max_length=250,
                             blank=True,
                             null=True,
                             db_index=True,
                             unique=True,
                             default=None)

    payer_id = models.CharField(max_length=250,
                                blank=True,
                                null=True,
                                default=None)

    date_created = models.DateTimeField(auto_now_add=True,
                                        help_text=_("Creation date"))

    date_after_set = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        help_text=_("Date after SetExpressCheckout was successfully called"))

    date_paid = models.DateTimeField(
        help_text=_("Date after DoExpressCheckout was successfully called"),
        default=None,
        null=True)

    completed = models.BooleanField(default=False)

    buyer_email = models.EmailField(blank=True, null=True, default=None)

    buyer_country = models.CharField(max_length=100,
                                     blank=True,
                                     null=True,
                                     default=None)

    buyer_first_name = models.CharField(max_length=200,
                                        blank=True,
                                        null=True,
                                        default=None)

    buyer_last_name = models.CharField(max_length=200,
                                        blank=True,
                                        null=True,
                                        default=None)

    set_ec_correlation_id = models.CharField(max_length=200,
                                             blank=True,
                                             null=True,
                                             default=None)

    do_ec_correlation_id = models.CharField(max_length=200,
                                            blank=True,
                                            null=True,
                                            default=None)
