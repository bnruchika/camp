from django.conf.urls import url
from django.contrib.auth import views as auth_views

from usermanagement.views import register, login_view, profile

urlpatterns = [
    url(r'register/', register, name="base_registration"),
    url(r'^login/$', login_view, name='login'),
    url(r'^profile/$', profile, name='profile'),

    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'usermanagement/logged_out.html'}, name="logout"),
]
