from django.shortcuts import render, redirect
from .models import AnnouncedPUResults, LGAS, PollingUnits, Party
from django.db.models import Sum
from django.http import JsonResponse

# Create your views here.

def home_page(request):

    return render(request, 'base/index.html')


def individual_polling(request, polling_unit_id):

    polling_unit_result = AnnouncedPUResults.objects.filter(polling_unit_uniqueid=polling_unit_id)

    context ={
        'result': polling_unit_result,
    }

    return render(request, 'base/index.html', context)

def lga_results(request):
    lgas = LGAS.objects.all()
    results = None
    selected_lga = None  

    if request.method == "GET" and "lga_id" in request.GET:
        lga_id = request.GET.get("lga_id")

        # Get selected LGA
        selected_lga = LGAS.objects.filter(lga_id=lga_id).first()

        if selected_lga:
            # Get all polling units under this LGA
            polling_units = PollingUnits.objects.filter(lga=selected_lga)

            # Sum total votes for each party from all polling units
            results = (
                AnnouncedPUResults.objects.filter(polling_unit_uniqueid__in=polling_units)
                .values("party_abbreviation")
                .annotate(total_votes=Sum("party_score"))
            )

    context = {
        "lgas": lgas,
        "results": results,
        "selected_lga": selected_lga,
    }
    
    return render(request, "base/lga_results.html", context)

def add_polling_unit_results(request):
    if request.method == "POST":
        lga_id = request.POST.get("lga_id")
        polling_unit_id = request.POST.get("polling_unit")

        if not lga_id:
            return JsonResponse({"error": "Missing lga_id"}, status=400)

        if not polling_unit_id:
            return JsonResponse({"error": "Missing polling_unit_id"}, status=400)

        # Fetch polling unit
        polling_unit = PollingUnits.objects.filter(lga_id=lga_id, pk=polling_unit_id).first()
        if not polling_unit:
            return JsonResponse({"error": "Invalid polling_unit_id for the given lga_id"}, status=400)

        # Save results
        parties = Party.objects.all()
        for party in parties:
            party_score = request.POST.get(f"party_{party.partyid}")
            if party_score is not None:
                AnnouncedPUResults.objects.create(
                    polling_unit=polling_unit,
                    party=party,
                    party_score=int(party_score)
                )

                return redirect('success_page')

    return render(request, "base/add_vote.html", {"lgas": LGAS.objects.all(), "parties": Party.objects.all()})

def get_polling_units(request):
    lga_id = request.GET.get('lga_id')  # Get LGA ID from request
    if not lga_id:
        return JsonResponse({"error": "Missing lga_id"}, status=400)

    polling_units = PollingUnits.objects.filter(lga_id=lga_id).values("polling_unit_id", "polling_unit_name")
    
    return JsonResponse(list(polling_units), safe=False)



def success_page(request):

    return render(request, 'base/success_page.html')
