=================
django-googleauth
=================

Simplified OAuth + OpenID Connect for authentication via Google.

googleauth used to be REALLY simple, but then Google decided to get rid of their OpenID service. Boooo Google. googleauth has been migrated to `OAuth 2.0 + OpenID Connect <https://developers.google.com/accounts/docs/OAuth2Login>`_, which isn't quite as great because it takes a bit more configuration to get going.

googleauth was built to provide an easy way to add authentication against a Google Apps for Business domain, ideally for an individual organization. This package is not the best option if you are looking for a general social auth solution. Check out `python-social-auth <https://pypi.python.org/pypi/python-social-auth>`_ instead.


Getting things set up on Google
===============================

#. Log in to the `Google API Console <https://code.google.com/apis/console>`_.

#. Open an existing project or create a new one if needed.

#. Under the *APIS & AUTH* menu item, click *APIs*.

#. Turn on the Google+ API.

#. Under the *APIS & AUTH* menu item, click *Credentials*.

#. Click the *Create new Client ID* button.

#. Select *Web application* for application type, add your domain as the JavaScript origin, and add the full domain and path to the OAuth callback (see below for how to find this URL). Click the *Create Client ID* button to finish.

#. You're going to need the Client ID and Client secret values in Django settings, so keep this window open or copy them for later.


Callback URL
~~~~~~~~~~~~

The callback URL is constructed from your preferred URL scheme, the domain at which your site is hosted, and the path where you mount the googleauth URL config in Django.

Let's assume you are using HTTPS and have mounted the googleauth URL config at the root URL. Your callback URL would look something like::

    https://<your-domain>/callback/

Okay, now let's assume you are using HTTP and have mounted the googleauth URL config under */accounts/*::

    http://<your-domain>/accounts/callback/


Django Setup
============

Settings and configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

The following settings should be placed in *settings.py*.

Add to *INSTALLED_APPS*::

    INSTALLED_APPS = (
        ...
        'googleauth',
        ...
    )

Add to *AUTHENTICATION_BACKENDS*::

    AUTHENTICATION_BACKENDS = (
        'googleauth.backends.GoogleAuthBackend',
        ...
    )

Required settings::

    # client ID from the Google Developer Console
    GOOGLEAUTH_CLIENT_ID = ''

    # client secret from the Google Developer Console
    GOOGLEAUTH_CLIENT_SECRET = ''

    # your app's domain, used to construct callback URLs
    GOOGLEAUTH_CALLBACK_DOMAIN = ''



Optional settings::

    # callback URL uses HTTPS (your side, not Google), default True
    GOOGLEAUTH_USE_HTTPS = True

    # restrict to the given Google Apps domain, default None
    GOOGLEAUTH_APPS_DOMAIN = ''

    # get user's name, default True (extra HTTP request)
    GOOGLEAUTH_GET_PROFILE = True

    # sets value of user.is_staff for new users, default False
    GOOGLEAUTH_IS_STAFF = False

    # list of default group names to assign to new users
    GOOGLEAUTH_GROUPS = []

URL routes
~~~~~~~~~~

Add URL config::

    urlpatterns = patterns('',
        ...
        (r'^auth/', include('googleauth.urls')),
        ...
    )

googleauth doesn't need to be mounted under */auth/*, it can go anywhere. Place it where you see fit for your specific app.