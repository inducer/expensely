from django.db.models.signals import post_save
from expenses.models import Entry
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def entry_saved(sender, instance, created, raw, **kwargs):
    if raw:
        return

    for component in instance.components.all():
        if component.account.guardian is None:
            continue

        msg = render_to_string("expenses/notification-email.txt",
                {
                    "created": created,
                    "component": component,
                    "entry": instance,
                    },
                request=None, using=None)

        send_mail(
            "[Expensely] %s in %s: %s"
            % (
                "Added" if created else "Updated",
                component.account.symbol,
                instance.description),
            msg,
            settings.ROBOT_FROM_EMAIL,
            [component.account.guardian.email])


post_save.connect(entry_saved, sender=Entry)

# vim: foldmethod=marker
