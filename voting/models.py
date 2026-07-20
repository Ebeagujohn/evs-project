from django.db import models
from voters.models import Voter
from candidates.models import Candidate
from django.utils import timezone


class Vote(models.Model):
    """
    A single cast vote. voter is OneToOneField (not ForeignKey) — this is
    what enforces "one vote per voter" at the database level, not just in
    view logic.
    """

    voter = models.OneToOneField(Voter, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.voter.voter_id} -> {self.candidate.name}"

class ElectionSettings(models.Model):
    """
    Controls the voting window. There is only ever ONE row of this model —
    save() always writes to pk=1, so no matter how many times an admin
    updates the schedule, it overwrites the same single record instead of
    creating new ones.
    """

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # the singleton row is never deleted

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(
            pk=1,
            defaults={
                "start_time": timezone.now(),
                "end_time": timezone.now() + timezone.timedelta(days=1),
            },
        )
        return obj

    @property
    def status(self):
        now = timezone.now()
        if now < self.start_time:
            return "not_started"
        if now > self.end_time:
            return "closed"
        return "open"

    def __str__(self):
        return f"Election window: {self.start_time} to {self.end_time}"    
