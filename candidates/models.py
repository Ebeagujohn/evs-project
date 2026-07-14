from django.db import models


class Candidate(models.Model):
    """A candidate contesting for a position — added dynamically by Admin."""

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, default="Governor")
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.position}"
