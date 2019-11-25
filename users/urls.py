from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    # url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]