from django.shortcuts import render,redirect

# Create your views here.


def landingpage(response):
    return render(response, 'main/landingpage.html')