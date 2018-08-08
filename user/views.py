from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, View, TemplateView, CreateView
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse
from geetest import GeetestLib

from user.forms import UserRegisterForm, UserLoginForm


class GeeTestMixin(object):
    gid = settings.GEETEST_ID
    gkey = settings.GEETEST_KEY

    def check_request(self, request):
        gt = GeetestLib(self.gid, self.gkey)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            return gt.success_validate(challenge, validate, seccode, user_id)
        return gt.failback_validate(challenge, validate, seccode)


class RegisterView(CreateView, GeeTestMixin):
    template_name = 'login_and_register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('user:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': '注册'
        })
        return context

    def form_valid(self, form):
        super().form_valid(form)
        messages.add_message(self.request, messages.INFO, '激活邮件已发出，请检查您的邮箱')
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        if not self.check_request(request):
            messages.add_message(request, messages.ERROR, '验证失败')
            return HttpResponseRedirect(reverse_lazy('user:register'))
        return super().post(request, *args, **kwargs)


class LoginView(FormView, GeeTestMixin):
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
        if not self.check_request(request):
            messages.add_message(request, messages.ERROR, '验证失败')
            return HttpResponseRedirect(reverse_lazy('user:login'))

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


class GtValidateView(View, GeeTestMixin):

    def get(self, request):
        user_id = 'test'
        gt = GeetestLib(self.gid, self.gkey)
        status = gt.pre_process(user_id)
        request.session[gt.GT_STATUS_SESSION_KEY] = status
        request.session["user_id"] = user_id
        response_str = gt.get_response_str()
        return HttpResponse(response_str)
