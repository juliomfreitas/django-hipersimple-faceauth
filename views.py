# -*- coding:utf-8 -*-
from urllib import urlencode
import requests
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def parse_query_string(string):
    return dict(
        map(lambda x: (x.split('=')[0], x.split('=')[1]),
            string.text.split('&'))
    )


class LoginFacebookBaseView(TemplateView):
    app_code = ''
    app_secret = ''

    name_url = ''

    def get(self, request, *args, **kwargs):

        login_code = request.REQUEST.get('code')

        if not login_code:
            return redirect('https://www.facebook.com/v2.3/dialog/oauth?' + urlencode(
                {'client_id': self.app_code, 'redirect_uri':
                 request.build_absolute_uri(reverse(self.name_url)),
                 'scope': 'public_profile,email'}
            ))

        token_data = requests.get(
            'https://graph.facebook.com/v2.3/oauth/access_token?' +
            urlencode({'client_id': self.app_code,
                       'redirect_uri':
                       request.build_absolute_uri(reverse(self.name_url)),
                       'client_secret': self.app_secret,
                       'code': login_code
                       })
        )

        if token_data.status_code != 200:
            return self.process_error(request)

        # API v2.3 returns a JSON, according to the documents linked at issue
        # #592, but it seems that this needs to be enabled(?), otherwise the
        # usual querystring type response is returned.
        # <https://github.com/omab/python-social-auth/blob/master/social/backends/facebook.py>
        try:
            token = token_data.json()['access_token']
        except ValueError:
            token = parse_query_string(token_data.text)['access_token']

        user_data = requests.get(
            'https://graph.facebook.com/v2.4/me',
            params={'access_token': token, 'fields': 'name,email', 'debug': 'all'}
        ).json()

        if not user_data.get('email'):
            return self.process_error(request)

        return self.process_success(request, user_data)
