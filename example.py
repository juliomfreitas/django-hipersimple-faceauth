# -*- coding: utf-8 -*-

# urls.py
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    '',
    url(
        r'^login-facebook/$',
        SimpleAuthFacebookView.as_view(),
        name='facebook-logincallback'),
)


# views.py

from views import AuthFacebookBaseView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class SimpleAuthFacebookView(AuthFacebookBaseView):
    # avoid access database on server load
    app_code = 'XXXXAAAAAAAACCCCC'
    app_secret = 'XXXXAAAAAAAACCCCCXXXXAAAAAAAACCCCC'

    # name of the url facebook will return (point to this same view)
    name_url = 'facebook-logincallback'

    def process_error(self, request):
        return redirect(reverse('page-error'))

    def process_success(self, request, user):
        # return to some protected page
        # you can save some kind of state to prevent not authorized access
        print user

        return redirect(reverse('areacliente-meuspedidos'))
