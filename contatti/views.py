from django.shortcuts import render

def contatti(request):
    return render(
        request,
        'contatti.html'
    )
