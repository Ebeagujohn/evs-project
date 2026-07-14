from django.db import models


class Voter(models.Model):
    """A registered class member — may or may not yet be eligible to vote."""

    ELIGIBLE = "Eligible"
    NOT_ELIGIBLE = "Not Eligible Yet"
    ELIGIBILITY_CHOICES = [
        (ELIGIBLE, "Eligible"),
        (NOT_ELIGIBLE, "Not Eligible Yet"),
    ]

    voter_id = models.CharField(max_length=20, unique=True, editable=False)
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    class_arm = models.CharField(max_length=50, blank=True)
    eligibility_status = models.CharField(
        max_length=20, choices=ELIGIBILITY_CHOICES, editable=False
    )
    has_voted = models.BooleanField(default=False)
    date_registered = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-generate voter_id and set eligibility on first save only.
        if not self.voter_id:
            self.eligibility_status = (
                self.ELIGIBLE if self.age >= 18 else self.NOT_ELIGIBLE
            )
            super().save(*args, **kwargs)  # save once to get a real pk
            self.voter_id = f"EVS-2026-{self.pk:04d}"
            super().save(update_fields=["voter_id"])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.voter_id})"
