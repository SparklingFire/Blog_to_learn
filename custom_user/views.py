from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth import logout, login, authenticate
from django.views import generic
from .forms import LoginForm
from .models import CustomUser


class LogoutView(generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return self.request.META.get('HTTP_REFERER','/')

    def dispatch(self, request, *args, **kwargs):
        logout(self.request)
        return super().dispatch(request, *args, **kwargs)


class LoginView(generic.FormView):
    form_class = LoginForm
    template_name = 'user/login.html'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(reverse('article-list'))
        return super().dispatch(request, *args, **kwargs)


class UserInfoView(generic.TemplateView):
    user = None
    template_name = None

    def get_template_names(self):
        if self.user == self.request.user:
            self.template_name = 'user/full_user_info.html'
        else:
            self.template_name = 'user/user_info.html'
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['articles'] = self.user.get_user_articles()
        ctx['comments'] = self.user.get_user_comments()
        ctx['tag'] = self.user.get_user_tag()
        ctx['rating'] = self.user.get_user_rating()
        return ctx

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(CustomUser, username=kwargs['username'])
        self.user.update_subscriptions()
        return super().dispatch(request, *args, **kwargs)
