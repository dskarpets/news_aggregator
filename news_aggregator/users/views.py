from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from .forms import RegisterForm, LoginForm, ProfileUpdateForm, CustomPasswordChangeForm


def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('news:index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Registration successful!'))
            return redirect('news:index')
        else:
            messages.error(request, _('Registration failed. Please check the form.'))
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('news:index')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, _('Login successful!'))

            if user.is_superuser:
                return redirect('admin:index')

            next_url = request.GET.get('next', 'news:index')
            return redirect(next_url)
        else:
            messages.error(request, _('Invalid username or password.'))
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view."""
    logout(request)
    messages.info(request, _('You have been logged out.'))
    return redirect('news:index')


@login_required
def profile_view(request):
    """User profile view."""
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin:index')

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile updated successfully!'))
            return redirect('users:profile')
        else:
            messages.error(request, _('Failed to update profile.'))
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})


@login_required
def change_password_view(request):
    """Change password view."""
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin:index')
    
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Password changed successfully!'))
            return redirect('users:profile')
        else:
            messages.error(request, _('Failed to change password.'))
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'users/change_password.html', {'form': form})
