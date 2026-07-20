from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.db.models import Count
from django.contrib import messages
from evs_project.decorators import admin_required
from .forms import VoterLoginForm, VoteForm, ElectionSettingsForm
from voters.models import Voter
from candidates.models import Candidate
from voting.models import Vote, ElectionSettings


def voting_login(request):
    """Handle voter login via Voter ID (FR4).

    Security fix: once a session is tied to a voter, this page no longer
    accepts a different Voter ID — it sends them straight to the ballot
    instead. They must explicitly log out to use a different ID."""

    election = ElectionSettings.load()
    if election.status != "open":
        return render(request, "voting/closed.html", {"election": election, "status": election.status})

    if request.session.get("voter_pk"):
        return redirect("voting:voting_cast_vote")

    if request.method == "POST":
        form = VoterLoginForm(request.POST)
        if form.is_valid():
            request.session["voter_pk"] = form.voter.pk
            return redirect("voting:voting_cast_vote")
    else:
        prefill_id = request.GET.get("voter_id", "")
        form = VoterLoginForm(initial={"voter_id": prefill_id})

    return render(request, "voting/login.html", {"form": form, "election": election})


def voting_logout(request):
    """Clears the current voting session."""
    request.session.pop("voter_pk", None)
    return redirect("voting:voting_login")


def voting_cast_vote(request):
    """Cast a vote for Governor (FR5). Every failure path clears the
    session before redirecting to login, to avoid an infinite loop with
    voting_login's new auto-redirect."""

    election = ElectionSettings.load()
    if election.status != "open":
        return render(request, "voting/closed.html", {"election": election, "status": election.status})

    voter_pk = request.session.get("voter_pk")
    if not voter_pk:
        return redirect("voting:voting_login")

    try:
        voter = Voter.objects.get(pk=voter_pk)
    except Voter.DoesNotExist:
        request.session.pop("voter_pk", None)
        return redirect("voting:voting_login")

    if voter.eligibility_status != Voter.ELIGIBLE or voter.has_voted:
        request.session.pop("voter_pk", None)
        return redirect("voting:voting_login")

    if request.method == "POST":
        form = VoteForm(request.POST)
        if form.is_valid():
            candidate = form.cleaned_data["candidate"]
            try:
                Vote.objects.create(voter=voter, candidate=candidate)
            except IntegrityError:
                request.session.pop("voter_pk", None)
                return redirect("voting:voting_login")

            voter.has_voted = True
            voter.save()
            del request.session["voter_pk"]
            return redirect("voting:voting_results")
    else:
        form = VoteForm()

    return render(request, "voting/cast_vote.html", {"voter": voter, "form": form})


@admin_required
def voting_results(request):
    results = Candidate.objects.annotate(vote_count=Count("vote")).order_by("-vote_count")
    total_voters = Voter.objects.count()
    total_votes_cast = Vote.objects.count()
    turnout_percent = round((total_votes_cast / total_voters * 100), 1) if total_voters else 0

    context = {
        "results": results,
        "total_voters": total_voters,
        "total_votes_cast": total_votes_cast,
        "turnout_percent": turnout_percent,
    }
    return render(request, "voting/results.html", context)


@admin_required
def election_settings(request):
    election = ElectionSettings.load()

    if request.method == "POST":
        form = ElectionSettingsForm(request.POST, instance=election)
        if form.is_valid():
            form.save()
            messages.success(request, "Election schedule updated.")
            return redirect("voting:voting_election_settings")
    else:
        form = ElectionSettingsForm(instance=election)

    return render(request, "voting/election_settings.html", {"form": form, "election": election})