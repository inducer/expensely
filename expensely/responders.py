from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib import messages


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, 'Logged out.')
