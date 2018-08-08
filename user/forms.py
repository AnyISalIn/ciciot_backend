from django import forms
from django.conf import settings
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.contrib.auth import password_validation
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator


def get_field_attrs(placeholder, textarea=False):
    ret = {'class': 'form-control form-control-lg', 'placeholder': placeholder.lower()}
    if textarea:
        ret.update({'rows': 20})
    return ret


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(get_field_attrs('Password')),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(get_field_attrs('Confirm Password')),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(get_field_attrs('Username')),
            'email': forms.EmailInput(get_field_attrs('Email')),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            raise forms.ValidationError('A user with that email already exists.')
        self.instance.email = email
        return email

    def save(self, *args, **kwargs):
        self.instance.is_active = False
        super().save(self, *args, **kwargs)
        send_mail(
            '请激活您的账户 -- 物联网技术应用',
            '点击以下链接激活您的账户 http://www.ciciot.com{}'.format(
                reverse_lazy('user:active',
                             kwargs={'uidb64': urlsafe_base64_encode(force_bytes(self.instance.pk)).decode(),
                                     'token': default_token_generator.make_token(self.instance)})),
            settings.EMAIL_FROM,
            [self.instance.email]
        )
        return self.instance


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(get_field_attrs('Email')),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(get_field_attrs('Password')),
    )
