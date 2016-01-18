## coding=utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from django.conf.urls import url

import views

urlpatterns = [
    url(r'^return/$', views.return_url),
    url(r'^cancel/$', views.cancel_url),
]
