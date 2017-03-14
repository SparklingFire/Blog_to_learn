from django.conf.urls import url
from . import views

urlpatterns = [
    url('^logout/$',
        view=views.LogoutView.as_view(),
        name='logout'),

    url('^login/$',
        view=views.LoginView.as_view(),
        name='login'),

    url('^(?P<username>[\w]+)/user_info/$',
        view=views.UserInfoView.as_view(),
        name='user-info')
]
