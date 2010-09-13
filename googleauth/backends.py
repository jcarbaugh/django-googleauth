from django.conf import settings
from django.contrib.auth.models import User

IS_STAFF = getattr(settings, 'GOOGLEAUTH_IS_STAFF', True)
DOMAIN = getattr(settings, 'GOOGLEAUTH_DOMAIN', None)

class GoogleAuthBackend(object):
    
    def authenticate(self, identifier=None, attributes=None):
        
        email = attributes.get('email', None)
        (username, domain) = email.split('@')
        
        if DOMAIN and DOMAIN != domain:
            return None
        
        try:
            
            user = User.objects.get(email=email)
            
        except User.DoesNotExist:
            
            user = User.objects.create(username=username, email=email)
            user.first_name = attributes.get('firstname', None)
            user.last_name = attributes.get('lastname', None)
            user.is_staff = IS_STAFF
            user.set_unusable_password()
            user.save()
        
        return user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass