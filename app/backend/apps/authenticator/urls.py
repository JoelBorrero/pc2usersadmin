from django.urls import path, include
from rest_framework import routers
from .viewsets import AuthenticatorViewSet

router = routers.DefaultRouter()
router.register(r'authenticator', AuthenticatorViewSet, basename='authenticator')
urlpatterns = [
    path(r'', include(router.urls))
]
