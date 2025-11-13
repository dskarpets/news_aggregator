from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class RegisterForm(UserCreationForm):
    """User registration form."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': _('Email')
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': _('Username')
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('Password')
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('Confirm Password')
        })


class LoginForm(AuthenticationForm):
    """User login form."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': _('Username')
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': _('Password')
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    """User profile update form."""
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    """Change password form."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('Old Password')
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('New Password')
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('Confirm New Password')
        })
