from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Poll, Choice, Vote
from django.db import models


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    return redirect('home')
            except IntegrityError:
                form.add_error('username', 'Username is already taken. Please choose a different one.')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})


@login_required(login_url='/login/')
def polls(request):
    return render(request, 'polls.html')


def logout_view(request):
    auth_logout(request)
    return redirect('home')


def user_logout(request):
    auth_logout(request)
    return redirect('home')


@login_required(login_url='/login/')
def poll_list(request):
    polls = Poll.objects.all()
    return render(request, 'poll_list.html', {'polls': polls})


@login_required(login_url='/login/')
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choices = poll.choices.all()  # Accessing choices associated with the poll
    return render(request, 'poll_detail.html', {'poll': poll, 'choices': choices})


@login_required(login_url='/login/')
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    error_message = None  # Initialize error message
    if request.method == 'POST':
        try:
            selected_choice_id = request.POST['choice']
            selected_choice = poll.choices.get(pk=selected_choice_id)
        except (KeyError, Choice.DoesNotExist):
            error_message = "You didn't select a choice."
        else:
            # Check if the user has already voted for this poll
            if Vote.objects.filter(user=request.user, choice__poll=poll).exists():
                error_message = "You have already voted in this poll."
            else:
                # Create a new Vote instance
                selected_choice.votes += 1
                selected_choice.save()
                # Record the vote for the user
                Vote.objects.create(user=request.user, choice=selected_choice)
                return HttpResponseRedirect(reverse('poll_results', args=(poll.id,)))
    return render(request, 'poll_detail.html', {
        'poll': poll,
        'error_message': error_message,
    })


@login_required(login_url='/login/')
def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'poll_results.html', {'poll': poll})
