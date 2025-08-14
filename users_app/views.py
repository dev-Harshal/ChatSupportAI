from django.shortcuts import render, redirect

def index_view(request):
    return redirect('users_app:login-view')

def login_view(request):
    return render(request, 'login.html')
