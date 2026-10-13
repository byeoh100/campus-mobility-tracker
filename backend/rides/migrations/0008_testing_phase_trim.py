"""Testing phase: trim what's already stored.

Each existing ride's rider name is replaced with a ride ID, and its email
and notes are erased (Ride.save keeps new rides the same way). Only the data
changes, not the tables. This can't be undone: the erased details aren't kept
anywhere.
"""

import secrets

from django.db import migrations

ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def trim(apps, schema_editor):
    Ride = apps.get_model("rides", "Ride")
    used = set()
    for ride in Ride.objects.only("id").iterator():
        ride_id = None
        while ride_id is None or ride_id in used:
            ride_id = "".join(secrets.choice(ALPHABET) for _ in range(6))
        used.add(ride_id)
        Ride.objects.filter(pk=ride.pk).update(rider_name=ride_id, rider_email="", notes="")


class Migration(migrations.Migration):

    dependencies = [
        ("rides", "0007_ride_series"),
    ]

    operations = [
        migrations.RunPython(trim, migrations.RunPython.noop),
    ]
