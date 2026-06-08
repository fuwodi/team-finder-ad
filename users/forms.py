from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm

from users.models import User
from users.validators import validate_github_url, validate_phone_format


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=124, label="Имя")
    surname = forms.CharField(max_length=124, label="Фамилия")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def save(self):
        return User.objects.create_user(
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
            name=self.cleaned_data["name"],
            surname=self.cleaned_data["surname"],
        )


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            self.user_cache = authenticate(
                self.request,
                username=email,
                password=password,
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Неверный email или пароль",
                    code="invalid_login",
                )
        return cleaned_data

    def get_user(self):
        return self.user_cache


class ProfileEditForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=12,
        label="Телефон",
        required=True,
    )

    class Meta:
        model = User
        fields = ("name", "surname", "avatar", "about", "phone", "github_url")
        labels = {
            "name": "Имя",
            "surname": "Фамилия",
            "avatar": "Аватар",
            "about": "О себе",
            "github_url": "GitHub",
        }

    def clean_phone(self):
        phone = (self.cleaned_data.get("phone") or "").strip()
        if not phone:
            raise forms.ValidationError("Это поле обязательно.")

        phone = validate_phone_format(phone)
        alternate = f"8{phone[2:]}"
        qs = User.objects.filter(phone__in=[phone, alternate])
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                "Пользователь с таким номером телефона уже существует."
            )
        return phone

    def clean_github_url(self):
        return validate_github_url(self.cleaned_data.get("github_url", ""))


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Текущий пароль",
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Новый пароль",
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Подтвердите новый пароль",
    )
