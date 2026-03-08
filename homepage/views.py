from django.shortcuts import render

def home_page(request):
    return render(
        request,
        'homepage/home.html',
        {
            'categories': [],
            'products': []
        }
    )