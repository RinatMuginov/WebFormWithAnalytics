from django.shortcuts import render, redirect

def profilepage(request):
    return render(request, 'profile_page.html')