"""Testing-phase data trim: rides keep a ride ID instead of the rider's name
and no email or notes; drivers keep a first name only and no phone; sign-in
keeps no names. Existing data is trimmed by migrations."""

from datetime import timedelta
from unittest import mock

from django.contrib.auth import get_user_model
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase, override_settings
from django.utils import timezone

from accounts.models import AdminEmail, Driver

from .models import RIDE_ID_ALPHABET, Ride

User = get_user_model()


def ride(**extra):
    return Ride.objects.create(
        rider_phone="8055550101", pickup_time=timezone.now() + timedelta(days=1),
        pickup_name="Library", dropoff_name="UCen", **extra,
    )


class SavingTests(TestCase):
    def test_any_save_keeps_a_ride_id_and_no_email_or_notes(self):
        r = ride(rider_name="Ana Lee", rider_email="ana@ucsb.edu", notes="Crutches")
        r.refresh_from_db()
        self.assertNotEqual(r.rider_name, "Ana Lee")
        self.assertEqual((r.rider_email, r.notes), ("", ""))
        ride_id = r.rider_name
        r.rider_name, r.notes = "Ana Lee", "Crutches"  # e.g. edited in the Django admin
        r.save()
        r.refresh_from_db()
        self.assertEqual((r.rider_name, r.notes), (ride_id, ""))

    def test_ride_ids_are_unique_and_readable(self):
        ids = [ride().rider_name for _ in range(50)]
        self.assertEqual(len(set(ids)), 50)
        for ride_id in ids:
            self.assertEqual(len(ride_id), 6)
            self.assertTrue(set(ride_id) <= set(RIDE_ID_ALPHABET), ride_id)
        self.assertFalse(set("01OI") & set(RIDE_ID_ALPHABET))  # no look-alikes

    def test_drivers_keep_a_first_name_and_no_phone(self):
        d = Driver.objects.create(email="dana@ucsb.edu", name="Dana Ortiz", phone="8055550123", color="#1a73e8")
        d.refresh_from_db()
        self.assertEqual((d.name, d.phone), ("Dana", ""))


@override_settings(ALLOWED_EMAIL_DOMAINS=["ucsb.edu"])
class ApiTests(TestCase):
    def setUp(self):
        AdminEmail.objects.create(email="boss@ucsb.edu")
        self.client.force_login(User.objects.create(username="boss@ucsb.edu", email="boss@ucsb.edu"))

    def test_names_emails_and_notes_sent_to_the_api_are_ignored(self):
        tomorrow = timezone.localdate() + timedelta(days=1)
        r = self.client.post("/api/rides/", {
            "rider_name": "Ana Lee", "rider_email": "ana@ucsb.edu", "notes": "Crutches",
            "rider_phone": "8055550101", "pickup_time": f"{tomorrow}T09:30",
            "pickup_name": "Library", "dropoff_name": "UCen",
        }, content_type="application/json")
        self.assertEqual(r.status_code, 201, r.json())
        ride_id = r.json()["rider_name"]
        self.assertRegex(ride_id, r"^[A-Z2-9]{6}$")
        self.assertEqual((r.json()["rider_email"], r.json()["notes"]), ("", ""))

        saved = Ride.objects.get()
        r = self.client.patch(f"/api/rides/{saved.id}/", {"rider_name": "Ana", "notes": "x"},
                              content_type="application/json")
        self.assertEqual((r.status_code, r.json()["rider_name"], r.json()["notes"]), (200, ride_id, ""))

    def test_google_sign_in_keeps_no_name(self):
        info = {"email": "boss@ucsb.edu", "email_verified": True, "given_name": "Ana", "family_name": "Lee"}
        with mock.patch("accounts.views.id_token.verify_oauth2_token", return_value=info), \
             override_settings(GOOGLE_CLIENT_ID="test"):
            r = self.client.post("/api/auth/google/", {"credential": "x"}, content_type="application/json")
        self.assertEqual(r.status_code, 200, r.content)
        user = User.objects.get(username="boss@ucsb.edu")
        self.assertEqual((user.first_name, user.last_name), ("", ""))


class MigrationTests(TransactionTestCase):
    """The migrations trim what's already in the database."""

    def migrate(self, *targets):
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        executor.migrate(list(targets))
        return executor.loader.project_state(list(targets)).apps

    def test_existing_data_is_trimmed(self):
        old = self.migrate(("rides", "0007_ride_series"), ("accounts", "0008_driver_purged_rides"))
        OldDriver, OldRide, OldUser = (old.get_model(*m) for m in (("accounts", "Driver"), ("rides", "Ride"), ("auth", "User")))
        driver = OldDriver.objects.create(email="d@ucsb.edu", name="Dana Ortiz", phone="8055550123", color="#1a73e8")
        for n in range(3):
            OldRide.objects.create(
                rider_name="Ana Lee", rider_email="ana@ucsb.edu", notes="Crutches", rider_phone="8055550101",
                pickup_time=timezone.now(), pickup_name="A", dropoff_name="B", driver_id=driver.id,
                link_token=f"token-{n}",
            )
        OldUser.objects.create(username="d@ucsb.edu", first_name="Dana", last_name="Ortiz")

        self.migrate(("rides", "0008_testing_phase_trim"), ("accounts", "0009_testing_phase_trim"))
        rides = list(Ride.objects.all())
        self.assertEqual({(r.rider_email, r.notes) for r in rides}, {("", "")})
        self.assertEqual(len({r.rider_name for r in rides}), 3)
        self.assertTrue(all(len(r.rider_name) == 6 and r.rider_name != "Ana Lee" for r in rides))
        self.assertEqual((Driver.objects.get().name, Driver.objects.get().phone), ("Dana", ""))
        self.assertEqual(User.objects.get(username="d@ucsb.edu").get_full_name(), "")
