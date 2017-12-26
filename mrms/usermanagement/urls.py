from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import register, login_view

urlpatterns = [
    url(r'register/',register, name="base_registration"),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'usermanagement/logged_out.html'}),
    ]
