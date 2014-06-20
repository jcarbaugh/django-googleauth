import random
from django.conf import settings
from django.core.urlresolvers import reverse

CSRF_CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def generate_csrf_token():
    return ''.join(random.choice(CSRF_CHARACTERS) for x in xrange(32))


def generate_redirect_uri():
    domain = getattr(settings, 'GOOGLEAUTH_DOMAIN', None)
    path = reverse('googleauth_callback')
    return 'https://%s%s' % (domain, path)
