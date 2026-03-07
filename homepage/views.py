from django.shortcuts import render

def home_page(request):
    return render(
        request,
        'body/home.html',
        {
            'categories': [],
            'products': []
        }
    )