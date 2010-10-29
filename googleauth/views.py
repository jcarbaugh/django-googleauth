from django.conf import settings
from django.contrib import auth
from django.contrib.auth.views import logout as django_logout
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from openid.consumer.consumer import Consumer
from openid.yadis.discover import DiscoveryFailure
import urllib

if hasattr(settings, 'GOOGLEAUTH_DOMAIN'):
    OPENID_ENDPOINT = "https://www.google.com/accounts/o8/site-xrds?hd=%s" % settings.GOOGLEAUTH_DOMAIN
else:
    OPENID_ENDPOINT = "https://www.google.com/accounts/o8/id"


def login(request):
    
    request.session['next'] = request.META.get('HTTP_REFERER', None)
    
    openid_consumer = Consumer(request.session, None)
    
    try:
        auth_request = openid_consumer.begin(OPENID_ENDPOINT)
    except DiscoveryFailure, df:
        return HttpResponse("%s" % df)

    # this is where attribute exchange stuff should be added
    extras = {
        "openid.ns.ax": "http://openid.net/srv/ax/1.0",
        "openid.ax.mode": "fetch_request",
        "openid.ax.required": "email,firstname,lastname",
        "openid.ax.type.email": "http://axschema.org/contact/email",
        "openid.ax.type.firstname": "http://axschema.org/namePerson/first",
        "openid.ax.type.lastname": "http://axschema.org/namePerson/last",
    }
    
    # generate callback URL
    
    scheme = 'https' if request.is_secure() else 'http'
    realm_default = 'localhost:8000' if settings.DEBUG else Site.objects.get_current().domain
    
    realm = '%s://%s' % (scheme, getattr(settings, 'GOOGLEAUTH_REALM', realm_default))
    cb_url = realm + reverse('googleauth.views.callback')
    
    # generate OpenID request redirect URL
    url = auth_request.redirectURL(realm, return_to=cb_url)
    
    return HttpResponseRedirect("%s&%s" % (url, urllib.urlencode(extras)))

def callback(request):
    
    identity = request.GET.get('openid.identity')
    
    attributes = {
        'firstname': request.GET.get('openid.ext1.value.firstname', None),
        'lastname': request.GET.get('openid.ext1.value.lastname', None),
        'email': request.GET.get('openid.ext1.value.email', None),
    }
    
    user = auth.authenticate(identifier=identity, attributes=attributes)
    if not user:
        return HttpResponseServerError('user account not found')
    auth.login(request, user)
    
    redirect = request.session.get('next', None)
    redirect_default = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
    return HttpResponseRedirect(redirect or redirect_default)

def logout(request):
    return django_logout(request)