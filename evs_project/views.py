from django.shortcuts import render
from django.http import HttpResponse

def healthz(request):
    return HttpResponse("ok")

def onboarding(request):
    """The very first screen a visitor sees — a short intro to the platform,
    followed by a choice: continue as Admin or as Voter."""
    return render(request, "onboarding.html")