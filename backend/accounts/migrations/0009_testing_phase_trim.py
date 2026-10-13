"""Testing phase: trim what's already stored.

Driver names are cut to their first word and driver phone numbers erased
(Driver.save keeps new drivers the same way), and the names Google sent at
sign-in are erased. Only the data changes, not the tables. This can't be
undone: the erased details aren't kept anywhere.
"""

from django.conf import settings
from django.db import migrations


def trim(apps, schema_editor):
    Driver = apps.get_model("accounts", "Driver")
    for driver in Driver.objects.all():
        first = (driver.name.split() or [""])[0]
        Driver.objects.filter(pk=driver.pk).update(name=first, phone="")
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    User.objects.exclude(first_name="", last_name="").update(first_name="", last_name="")


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_driver_purged_rides"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(trim, migrations.RunPython.noop),
    ]
