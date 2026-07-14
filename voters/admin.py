from django.contrib import admin
from .models import Voter

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ("voter_id", "full_name", "age", "eligibility_status", "has_voted")
    list_filter = ("eligibility_status", "has_voted")
    search_fields = ("voter_id", "full_name")
