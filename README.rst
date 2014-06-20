=================
django-googleauth
=================

Simplified OAuth + OpenID Connect for authentication via Google.

Settings
========

The following settings should be placed in *settings.py*.

===========================  ==============================================================
Setting                      Value
===========================  ==============================================================
GOOGLEAUTH_CLIENT_ID         client ID from the Google Developer Console
GOOGLEAUTH_CLIENT_SECRET     client secret from the Google Developer Console
GOOGLEAUTH_IS_STAFF          sets value of user.is_staff for new users, default False
GOOGLEAUTH_GROUPS            list of default group names to assign to new users
GOOGLEAUTH_DOMAIN            the app's domain, used to construct callback URLs
GOOGLEAUTH_DOMAIN_ONLY       True if only emails from the domain are allowed, default False
===========================  ==============================================================