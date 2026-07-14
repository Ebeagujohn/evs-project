from django.db import models
from voters.models import Voter
from candidates.models import Candidate


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
