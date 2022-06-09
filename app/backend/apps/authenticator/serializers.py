from .models import PC2User
from backend.apps.utils.serializers import CustomSerializer


class PC2UserSerializer(CustomSerializer):
    class Meta:
        model = PC2User
        exclude = []
