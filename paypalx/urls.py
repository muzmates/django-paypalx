## coding=utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from django.conf.urls import patterns, url

urlpatterns = patterns('paypalx.views',
    url(r'^return/$', 'return_url'),
    url(r'^cancel/$', 'cancel_url'),
)
