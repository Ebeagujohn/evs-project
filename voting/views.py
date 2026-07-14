from django.shortcuts import render

def voting_login(request):
    """Placeholder: Voter ID login (FR4). Person C builds this out."""
    return render(request, "voting/login.html")

def voting_cast_vote(request):
    """Placeholder: cast a vote, block duplicates (FR5). Person C builds this out."""
    return render(request, "voting/cast_vote.html")

def voting_results(request):
    """Placeholder: live results page (FR6). Person C builds this out."""
    return render(request, "voting/results.html")
