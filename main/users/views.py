from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import SignupForm


def signup(request):
    '''
    Signup for a new User account.
    '''

    form = SignupForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect('index')

    return render(request, 'users/signup.html', {
        'form': form
    })
