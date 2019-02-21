from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':    #what is going on with all caps POST?
        form = UserRegisterForm(request.POST)
        if form.is_valid():         #explained in video 7(?)
            form.save()             #how to save the user on your login page
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account Has been Created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required                     #requires user be logged in to see profile. Decoarators ad fuction to functions
def profile(request):               #creating an html view for the profile
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account Has been Updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {                     #passing it into a template via a dictionary
        'u_form': u_form,            #dictionary keys
        'p_form': p_form
    }      

    return render(request, 'users/profile.html', context)