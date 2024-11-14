import logging
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy
from django.contrib import messages
from rest_framework import generics
from django.contrib.auth import login, logout, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import *
from financeAPI.models import *
from .filters import *
from .serializers import ObjectSerializer, ProfileSerializer

logger = logging.getLogger(__name__)

User = get_user_model()


def index(request):
    if request.user.is_anonymous:
        return redirect('login')
    return redirect('profile')


def show_errors(request, form) -> None:
    errors_json = form.errors.as_json()
    errors_dict = json.loads(errors_json)

    for field, errors in errors_dict.items():
        for error in errors:
            message = error['message']
            messages.warning(request, gettext_lazy(message))
            logger.warning("Got an invalid %s form: %s", form.__class__.__name__, message)


class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated,]

    @staticmethod
    def get(request, ):
        user = request.user
        profile = Profile.objects.get(user=user)

        objective = Objective.objects.filter(user=user)

        if profile:
            serializer = ProfileSerializer(Profile.objects.filter(user=user),many=True, context={'request': request})
            return render(request, 'financeAPI/index.html', {'user': user, 'serializer': serializer.data,
                                                     'title': 'Главное меню', "objective": objective, 'form': SearchName(), })
        else:
            return redirect('crt_profile')


class ProfileCreate(APIView):
    @staticmethod
    def get(request):
        user = request.user
        form = ProfileForm(request.GET)
        data = {
            'user': user,
            'form': form,
            'title': "Создание профиля",
            'info': "Вам нужно создать профиль, чтобы вести свои расчеты.",
        }
        return render(request, 'financeAPI/crt_object.html', context=data)

    @staticmethod
    def post(request):
        user = request.user
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.user = user
            file.save()
            return redirect('profile')
        else:
            messages.error(request, gettext_lazy("Ошибка при сохранении цели"))
            return render(request, 'financeAPI/crt_object.html', context={'user': user, 'form': form})


class ProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, username: str):
        user = get_object_or_404(User, username=username)
        return get_object_or_404(Profile, user=user)

    def get(self, request, username: str):
        obj = self.get_object(username)
        form = ProfileForm(instance=obj)
        return render(request, 'financeAPI/crt_object.html', context={'user': request.user, 'form': form,
                                                                      "object": obj, 'title': 'Изменение профиля'})

    def post(self, request, username: str):
        obj = self.get_object(username)
        form = ProfileForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'financeAPI/crt_object.html', context={'object': obj,
                                                                      'form': form, 'user': request.user})




class LoginAPI(APIView):
    @staticmethod
    def get(request):
        if request.user.is_anonymous:
            form = LoginForm()
            data = {
                'form': form,
                'title': "Авторизация",
            }
            return render(request, 'financeAPI/login.html', context=data)
        logger.info("User %s tried to login" % request.user)
        messages.info(request, gettext_lazy(" (ЖопаЖопа) You are already logged in "))
        return redirect("profile")

    @staticmethod
    def post(request):
        form = LoginForm(data=request.data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                logger.info("User %s is logged in" % user)
                return redirect('profile')
            else:
                messages.warning(request, gettext_lazy("username or password incorrect"))
                logger.info("User with username %s is not found" % username)
                return redirect('login')
        show_errors(request, form)
        return redirect('login')


class RegisterAPI(APIView):
    """ Registration endpoint """

    @staticmethod
    def get(request):
        if request.user.is_anonymous:
            form = RegisterForm()
            return render(request, 'financeAPI/register.html', {'form': form, 'title': 'Регистрация аккаунта'})
        logger.info("User %s tried to access registration page" % request.user)
        messages.info(request, gettext_lazy("You are already logged in"))
        return redirect("profile")

    @staticmethod
    def post(request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            if User.objects.filter(email=email).exists():
                messages.error(request, gettext_lazy("Email уже существует. Пожалуйста, используйте другой."))
                return render(request, 'financeAPI/register.html', {'form': form})

            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, gettext_lazy("Вы успешно зарегистрированы! Вы можете войти в свой аккаунт."))
            return redirect('login')

        else:
            show_errors(request, form)
            return render(request, 'financeAPI/register.html', {'form': form})

class LogoutView(APIView):
    """
    Logout endpoint
    """

    @staticmethod
    def get(request):
        if not request.user.is_anonymous:
            logger.info("Logout user %s" % request.user)
            logout(request)
        else:
            logger.info("Anonymous user try to log out")
        return redirect('login')


class ObjectAPI(APIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request):
        user = request.user
        objective_filter = ObjectFilter(request.GET, queryset=Objective.objects.filter(user=user))
        # фильтр помогает избежать несколько строчек кода одной строкой
        # form = SearchName()
        #
        # objectives = Objective.objects.filter(user=user)
        #
        # object_filter = request.GET.get('object')
        # if object_filter:
        #     objectives = objectives.filter(object__icontains=object_filter)

        serializer = ObjectSerializer(objective_filter.qs, many=True, context={'request': request})
        data = {
            'title': "Ваши цели",
            'user': user,
            'serializer': serializer.data,
            'filter': objective_filter,
        }
        return render(request, 'financeAPI/object.html', context=data)


class ObjectCreate(APIView):
    permission_classes = [IsAuthenticated, ]

    @staticmethod
    def get(request):
        user = request.user
        form = ObjectForm(request.GET)
        data = {
            'title': "Добавление цели",
            'user': user,
            'form': form,
        }
        return render(request, 'financeAPI/crt_object.html', context=data)

    @staticmethod
    def post(request):
        user = request.user
        form = ObjectForm(request.POST)

        if form.is_valid():
            file = form.save(commit=False)
            file.user = user
            file.save()
            return redirect('object')
        else:
            messages.error(request, gettext_lazy("Ошибка при сохранении цели"))
            return render(request, 'financeAPI/crt_object.html', context={'form': form,
                                                                          'errors': form.errors})
class ObjectUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, object_slug):
        return get_object_or_404(Objective, slug=object_slug)

    def get(self, request, object_slug: str):
        obj = self.get_object(object_slug)
        form = ObjectForm(instance=obj)
        user = request.user
        return render(request, 'financeAPI/crt_object.html', context={'object': obj,
                                                                      'form': form, 'user': user, 'title': 'Изменение записи'})

    #ПО ФАКТУ ЭТО PUT ЗАПРОС НО НУЖНО ЗАПИСЫВАТЬ КАК POST
    def post(self, request, object_slug: str):
        # Получаем объект по slug
        obj = self.get_object(object_slug)
        form = ObjectForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('object')
        return render(request, 'financeAPI/crt_object.html', context={'object': obj,
                                                                      'form': form, 'user': request.user})



class ObjectRemove(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, ]

    queryset = Objective.objects.all()
    serializer_class = ObjectSerializer

    def post(self, request, pk, *args):
        instance = get_object_or_404(Objective, pk=pk)
        instance.delete()
        return redirect('object')
