from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def signin(request):
    return render(request, 'signin.html')


def dashboard(request):
    return render(request, 'assessment/dashboard.html')
    