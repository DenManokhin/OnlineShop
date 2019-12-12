from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout


def signup_view(request):
    context = {}
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            context['form'] = form
    else:
        context['form'] = UserCreationForm()
    return render(request, 'signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')
