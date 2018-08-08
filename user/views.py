from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, View, TemplateView, CreateView
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User

from user.forms import UserRegisterForm, UserLoginForm


class RegisterView(CreateView):
    template_name = 'login_and_register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('user:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': '注册'
        })
        return context

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, '激活邮件已发出，请检查您的邮箱')
        return super().post(request, *args, **kwargs)


class LoginView(FormView):
    template_name = 'login_and_register.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': '登录'
        })
        return context

    def post(self, request, *args, **kwargs):
        data = self.get_form_kwargs()['data']
        email = data.get('email', None)
        password = data.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('home'))
            messages.add_message(request, messages.WARNING, '用户未激活')
        else:
            messages.add_message(request, messages.ERROR, '用户名或密码错误, 请重试')
        return render(request, self.template_name, self.get_context_data())


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('home'))


class ActiveView(View):

    def get(self, request, uidb64, token):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        if user:
            if default_token_generator.check_token(user, token):
                user.is_active = True
                messages.add_message(request, messages.SUCCESS, '用户激活成功')
            else:
                messages.add_message(request, messages.ERROR, 'Token 错误，用户激活失败')
        user.save()
        return render(request, 'login_and_register.html', {
            'form_title': '登录',
            'form': UserLoginForm,
        })
