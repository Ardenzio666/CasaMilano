from django.shortcuts import render

def chisiamo(request):
    return render(
        request,
        'chisiamo.html'
    )
