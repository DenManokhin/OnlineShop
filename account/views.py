from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from account.forms import SignUpForm, SignInForm


def signup_view(request):
    context = {}
    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            context['form'] = form
    else:
        context['form'] = SignUpForm()
    return render(request, 'signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def signin_view(request):
    context = {}
    user = request.user;

    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = SignInForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
    else:
        form = SignInForm()

    context['form'] = form
    return render(request, 'signin.html', context)
