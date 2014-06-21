import requests
from django.conf import settings
from django.contrib.auth.models import User, Group

IS_STAFF = getattr(settings, 'GOOGLEAUTH_IS_STAFF', False)
GROUPS = getattr(settings, 'GOOGLEAUTH_GROUPS', tuple())
APPS_DOMAIN = getattr(settings, 'GOOGLEAUTH_APPS_DOMAIN', None)


class GoogleAuthBackend(object):

    def authenticate(self, identifier=None, attributes=None):

        email = attributes.get('email', None)
        (username, domain) = email.split('@')

        if APPS_DOMAIN and APPS_DOMAIN != domain:
            return None

        try:

            try:

                user = User.objects.get(email=email)

            except User.MultipleObjectsReturned:

                user = User.objects.get(username=username, email=email)

        except User.DoesNotExist:

            user = User.objects.create(username=username, email=email)
            user.first_name = attributes.get('first_name') or ''
            user.last_name = attributes.get('last_name') or ''
            user.is_staff = IS_STAFF
            user.set_unusable_password()

            for group in GROUPS:
                try:
                    grp = Group.objects.get(name=group)
                    user.groups.add(grp)
                except:
                    pass

            user.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass
