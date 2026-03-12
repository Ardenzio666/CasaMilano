from django.shortcuts import render

def dovetrovarci(request):
    return render(
        request,
        'dovetrovarci.html'
    )
