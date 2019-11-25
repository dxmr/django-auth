from django.conf.urls import url

from users.api_views import SignUpAPIView, LoginAPIView

urlpatterns = [
    url(r'^signup/$', SignUpAPIView.as_view(), name='api_signup'),
    url(r'^login/$', LoginAPIView.as_view(), name='api_login'),
]
