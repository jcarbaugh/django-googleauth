import jwt
import requests
import urllib

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.views import logout as django_logout
from django.http import HttpResponse, HttpResponseRedirect

from .util import generate_csrf_token, generate_redirect_uri

GOOGLE_AUTH_ENDPOINT = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_ENDPOINT = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_USERINFO_ENDPOINT = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'

CLIENT_ID = getattr(settings, 'GOOGLEAUTH_CLIENT_ID', None)
CLIENT_SECRET = getattr(settings, 'GOOGLEAUTH_CLIENT_SECRET', None)
DOMAIN = getattr(settings, 'GOOGLEAUTH_DOMAIN', None)
DOMAIN_ONLY = getattr(settings, 'GOOGLEAUTH_DOMAIN_ONLY', False)


def login(request):

    request.session['next'] = request.META.get('HTTP_REFERER', None)

    csrf_token = generate_csrf_token()

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': 'openid email profile',
        'redirect_uri': generate_redirect_uri(),
        'state': csrf_token,
    }

    if DOMAIN_ONLY:
        params['hd'] = DOMAIN

    request.session['googleauth_csrf'] = csrf_token

    return HttpResponseRedirect("%s?%s" % (GOOGLE_AUTH_ENDPOINT, urllib.urlencode(params)))


def callback(request):

    if request.GET.get('state') != request.session.get('googleauth_csrf'):
        return HttpResponse('Invalid state parameter', status=401)

    code = request.GET.get('code')

    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': generate_redirect_uri(),
        'grant_type': 'authorization_code',
    }

    resp = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data)

    if resp.status_code != 200:
        return HttpResponse('Invalid token response', status=401)

    tokens = resp.json()
    id_token = jwt.decode(tokens['id_token'], verify=False)

    if not id_token['email_verified'] or id_token['iss'] != 'accounts.google.com' or id_token['aud'] != CLIENT_ID:
        return HttpResponse('Forged response', status=401)

    attributes = {
        'email': id_token.get('email'),
        'access_token': tokens['access_token'],
    }


    # get profile data

    headers = {'Authorization': 'Bearer %s' % attributes['access_token']}
    resp = requests.get(GOOGLE_USERINFO_ENDPOINT, headers=headers)
    if resp.status_code == 200:
        profile = resp.json()
        attributes['first_name'] = profile.get('given_name')
        attributes['last_name'] = profile.get('family_name')


    # authenticate user

    user = auth.authenticate(attributes=attributes)
    if not user:
        return HttpResponse('User account not found', status=404)
    auth.login(request, user)

    # redirect

    redirect = request.session.get('next', None)
    redirect_default = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
    return HttpResponseRedirect(redirect or redirect_default)


def logout(request):
    return django_logout(request)
