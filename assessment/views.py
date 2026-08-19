from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def signin(request):
    return render(request, 'signin.html')


def dashboard(request):
    return render(request, 'assessment/dashboard.html')


def aptitude_ready(request):
    return render(request, 'assessment/aptitude-ready.html')


def assess_aptitude(request):
    return render(request, 'assessment/aptitude-assess.html')


def preference_ready(request):
    return render(request, 'assessment/preference-ready.html')


def assess_preference(request):
    return render(request, 'assessment/preference-assess.html')


def result(request):
    return render(request, 'assessment/result.html')