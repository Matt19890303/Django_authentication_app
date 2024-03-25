from django.apps import AppConfig
from django.conf import settings


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    # This will be called once appis running
    def ready(self):
        # Important to import these after app has run
        # Otherwise we get circular import error
        from django.contrib.auth.models import Group
        from django.db.models.signals import post_save

        # After user modelis created run the below function/method
        def add_to_default_group(sender, **kwargs):
            # The instance is the user object that was created
            user = kwargs['instance']
            # Only add to default group if user is created
            if kwargs['created']:
                group, ok = Group.objects.get_or_create(name='Default')
                group.user_set.add(user)

        # After user modelis created and saved it calls the function created above
        post_save.connect(add_to_default_group, sender=settings.AUTH_USER_MODEL)