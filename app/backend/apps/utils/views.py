from django.http import HttpResponse
from django.template import loader
from rest_framework import permissions
from rest_framework.decorators import permission_classes

from backend.apps.authenticator.serializers import PC2UserSerializer


@permission_classes([permissions.IsAdminUser])
def authenticator(request):
    # serializer = PC2UserSerializer(brand)
    template = loader.get_template('auth.html')
    document = template.render({})
    return HttpResponse(document, status=200)