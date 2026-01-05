from django.contrib import messages
from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_logged_out


@receiver(user_logged_in)
def add_login_message(request, user, **kwargs):
    messages.success(request, f"Welcome back, {user.get_username()}.")


@receiver(user_logged_out)
def add_logout_message(request, user, **kwargs):
    messages.info(request, "You have been logged out.")
    pass
