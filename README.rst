=================
django-googleauth
=================

Simplified OAuth + OpenID Connect for authentication via Google.

Settings
========

The following settings should be placed in *settings.py*.

===========================  ================================================================
Setting                      Value
===========================  ================================================================
GOOGLEAUTH_USE_HTTPS         callback URL uses HTTPS (your side, not Google), default True
GOOGLEAUTH_CLIENT_ID         client ID from the Google Developer Console
GOOGLEAUTH_CLIENT_SECRET     client secret from the Google Developer Console
GOOGLEAUTH_CALLBACK_DOMAIN   the app's callback domain, used to construct callback URLs
GOOGLEAUTH_APPS_DOMAIN       restrict to the given Google Apps domain, default None
GOOGLEAUTH_GET_PROFILE       get user's name, default True (extra HTTP request)
GOOGLEAUTH_IS_STAFF          sets value of user.is_staff for new users, default False
GOOGLEAUTH_GROUPS            list of default group names to assign to new users
===========================  ================================================================