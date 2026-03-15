from django.shortcuts import render

def eventi(request):
    return render(
        request,
        'eventi.html'
    )
