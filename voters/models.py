from datetime import date
from django.db import models



GENDER_CHOICES = [
    ("Male", "Male"),
    ("Female", "Female"),
]

NIGERIA_STATES = [
    ("Abia", "Abia"), ("Adamawa", "Adamawa"), ("Akwa Ibom", "Akwa Ibom"),
    ("Anambra", "Anambra"), ("Bauchi", "Bauchi"), ("Bayelsa", "Bayelsa"),
    ("Benue", "Benue"), ("Borno", "Borno"), ("Cross River", "Cross River"),
    ("Delta", "Delta"), ("Ebonyi", "Ebonyi"), ("Edo", "Edo"),
    ("Ekiti", "Ekiti"), ("Enugu", "Enugu"), ("Gombe", "Gombe"),
    ("Imo", "Imo"), ("Jigawa", "Jigawa"), ("Kaduna", "Kaduna"),
    ("Kano", "Kano"), ("Katsina", "Katsina"), ("Kebbi", "Kebbi"),
    ("Kogi", "Kogi"), ("Kwara", "Kwara"), ("Lagos", "Lagos"),
    ("Nasarawa", "Nasarawa"), ("Niger", "Niger"), ("Ogun", "Ogun"),
    ("Ondo", "Ondo"), ("Osun", "Osun"), ("Oyo", "Oyo"),
    ("Plateau", "Plateau"), ("Rivers", "Rivers"), ("Sokoto", "Sokoto"),
    ("Taraba", "Taraba"), ("Yobe", "Yobe"), ("Zamfara", "Zamfara"),
    ("FCT", "Federal Capital Territory"),
]


class Voter(models.Model):
    """A registered voter. Only people aged 18–100 (computed from date of
    birth) ever get a Voter ID — anyone outside that range is rejected at
    registration and never saved (see forms.py). The age check in save()
    below is a second, defensive layer at the database level, in case a
    record is ever created another way (e.g. directly through the Django
    admin panel)."""

    ELIGIBLE = "Eligible"
    NOT_ELIGIBLE = "Not Eligible"
    ELIGIBILITY_CHOICES = [
        (ELIGIBLE, "Eligible"),
        (NOT_ELIGIBLE, "Not Eligible"),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    state_of_origin = models.CharField(max_length=50, choices=NIGERIA_STATES)
    photo = models.ImageField(upload_to="voter_photos/", blank=True)

    voter_id = models.CharField(
        max_length=20, unique=True, editable=False, blank=True, null=True
    )
    eligibility_status = models.CharField(
        max_length=20, choices=ELIGIBILITY_CHOICES, editable=False, default=ELIGIBLE
    )
    has_voted = models.BooleanField(default=False)
    date_registered = models.DateTimeField(auto_now_add=True)

    @property
    def age(self):
        today = date.today()
        years = today.year - self.date_of_birth.year
        had_birthday_this_year = (today.month, today.day) >= (
            self.date_of_birth.month,
            self.date_of_birth.day,
        )
        if not had_birthday_this_year:
            years -= 1
        return years

    def save(self, *args, **kwargs):
        is_first_save = self._state.adding
        is_eligible_age = 18 <= self.age <= 100
        self.eligibility_status = self.ELIGIBLE if is_eligible_age else self.NOT_ELIGIBLE

        if is_first_save and is_eligible_age:
            super().save(*args, **kwargs)
            self.voter_id = f"EVS-2026-{self.pk:04d}"
            super().save(update_fields=["voter_id"])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.voter_id or 'no ID'})"