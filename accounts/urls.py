# accounts/urls.py
from django.urls import path, include
from .views import SignUpView


urlpatterns = [
    # contains built-in urls & views for "signin" and "signout":
    path('', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
]