from django.shortcuts import render
from django.db.models import Q
from voters.models import Voter


def dashboard_voters_list(request):
    """
    Fully functional replacement for browsing voters via /admin/.
    Supports: search by name/voter_id, filter by eligibility status,
    and shows live summary counts.
    """

    voters = Voter.objects.all().order_by("-date_registered")

    query = request.GET.get("q", "").strip()
    if query:
        voters = voters.filter(
            Q(full_name__icontains=query) | Q(voter_id__icontains=query)
        )

    status_filter = request.GET.get("status", "")
    if status_filter in [Voter.ELIGIBLE, Voter.NOT_ELIGIBLE]:
        voters = voters.filter(eligibility_status=status_filter)

    total_voters = Voter.objects.count()
    eligible_count = Voter.objects.filter(eligibility_status=Voter.ELIGIBLE).count()
    not_eligible_count = Voter.objects.filter(eligibility_status=Voter.NOT_ELIGIBLE).count()
    voted_count = Voter.objects.filter(has_voted=True).count()

    context = {
        "voters": voters,
        "query": query,
        "status_filter": status_filter,
        "total_voters": total_voters,
        "eligible_count": eligible_count,
        "not_eligible_count": not_eligible_count,
        "voted_count": voted_count,
        "eligible_value": Voter.ELIGIBLE,
        "not_eligible_value": Voter.NOT_ELIGIBLE,
    }
    return render(request, "dashboard/voters_list.html", context)