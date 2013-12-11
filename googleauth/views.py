from django.conf import settings
from django.contrib import auth
from django.contrib.auth.views import logout as django_logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from openid.consumer.consumer import Consumer
from openid.yadis.discover import DiscoveryFailure
import urllib

def login(request):
    """ Redirect user to appropriate Google authentication URL.
        Uses attribute exchange to get user's name and email address.
    """
    
    request.session['next'] = request.META.get('HTTP_REFERER', None)
    
    openid_consumer = Consumer(request.session, None)
    
    # generate appropriate endpoint based on whether Google or Apps account is used
    if hasattr(settings, 'GOOGLEAUTH_DOMAIN'):
        endpoint = "https://www.google.com/accounts/o8/site-xrds?hd=%s" % settings.GOOGLEAUTH_DOMAIN
    else:
        endpoint = "https://www.google.com/accounts/o8/id"
    
    # try request
    try:
        auth_request = openid_consumer.begin(endpoint)
    except DiscoveryFailure, df:
        return HttpResponseServerError("%s" % df)

    # attribute exchange to get email, firstname, and lastname
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
    realm_default = 'localhost:8000' if settings.DEBUG else settings.ALLOWED_HOSTS[0]
    realm = '%s://%s' % (scheme, getattr(settings, 'GOOGLEAUTH_REALM', realm_default))
    cb_url = realm + reverse('googleauth.views.callback')
    
    # generate OpenID request redirect URL
    url = auth_request.redirectURL(realm, return_to=cb_url)
    
    return HttpResponseRedirect("%s&%s" % (url, urllib.urlencode(extras)))

def callback(request):
    """ Handle callback from Google authentication.
        Logs user in if the callback was successful.
    """
    
    identity = request.GET.get('openid.identity')
    
    # extract ax attributes from response
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
    """ Log user out of Django application.
        Does not log out of user's Google account.
    """
    return django_logout(request)
