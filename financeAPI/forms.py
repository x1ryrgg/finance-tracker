from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from financeAPI.models import User, Profile, Objective


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(), label_suffix='')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(), label_suffix='')

    class Meta:
        model = User
        fields = ('username', 'password')


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(), label_suffix='')
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(), label_suffix='')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(), label_suffix='')
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(), label_suffix='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('all_money', 'text', 'image')

    def clean_all_money(self):
        all_money = self.cleaned_data['all_money']
        if all_money is None:
            raise ValidationError('Заполните поле')
        return all_money


class ObjectForm(forms.ModelForm):
    object = forms.CharField(label='Название цели', widget=forms.TextInput(), label_suffix='')
    obj_money = forms.IntegerField(label='Сумма для цели', widget=forms.NumberInput(), label_suffix='')

    class Meta:
        model = Objective
        fields = ('object', 'obj_money')


class CalculateForm(forms.Form):
    years = forms.IntegerField(label='Количество лет', widget=forms.NumberInput(), label_suffix='')
    money_in_month = forms.IntegerField(label='Заробатная плата в месяц составляет', widget=forms.NumberInput(), label_suffix='')

