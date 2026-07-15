from django.shortcuts import render, redirect
from django.db import IntegrityError
from .forms import VoterLoginForm, VoteForm
from voters.models import Voter
from voting.models import Vote
from django.db.models import Count
from candidates.models import Candidate


def voting_login(request):
    """Handle voter login via Voter ID (FR4)."""
    if request.method == "POST":
        form = VoterLoginForm(request.POST)
        if form.is_valid():
            request.session["voter_pk"] = form.voter.pk
            return redirect("voting:voting_cast_vote")
    else:
        form = VoterLoginForm()
    return render(request, "voting/login.html", {"form": form})


def voting_cast_vote(request):
    """Cast a vote for Governor (FR5). Requires a valid session from voting_login."""

    voter_pk = request.session.get("voter_pk")
    if not voter_pk:
        return redirect("voting:voting_login")

    try:
        voter = Voter.objects.get(pk=voter_pk)
    except Voter.DoesNotExist:
        return redirect("voting:voting_login")

    # Re-check eligibility and vote status fresh from the DB — don't trust
    # the session alone, in case something changed since login.
    if voter.eligibility_status != Voter.ELIGIBLE or voter.has_voted:
        return redirect("voting:voting_login")

    if request.method == "POST":
        form = VoteForm(request.POST)
        if form.is_valid():
            candidate = form.cleaned_data["candidate"]
            try:
                Vote.objects.create(voter=voter, candidate=candidate)
            except IntegrityError:
                # The OneToOneField caught a duplicate vote (e.g. double
                # submit) at the database level — treat it the same as
                # already having voted.
                return redirect("voting:voting_login")

            voter.has_voted = True
            voter.save()
            del request.session["voter_pk"]
            return redirect("voting:voting_results")
    else:
        form = VoteForm()

    return render(request, "voting/cast_vote.html", {"voter": voter, "form": form})


def voting_results(request):
    """Live results page (FR6). Recomputed from the database on every load."""

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