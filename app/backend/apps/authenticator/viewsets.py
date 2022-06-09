import csv
import pandas as pd

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import PC2UserSerializer
from .models import PC2User


class AuthenticatorViewSet(viewsets.ModelViewSet):
    model = PC2User
    queryset = model.objects.all()
    serializer_class = PC2UserSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['GET'])
    def db_status(self, request):
        try:
            self.model.objects.all()
            return Response({'ok': True, 'description': 'Database working'}, status=status.HTTP_200_OK)
        except:
            return Response({'ok': False, 'description': 'Database connection loss'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    @action(detail=False, methods=['POST'])
    def register(self, request):
        fields = request.data
        user = self.model.objects.filter(username=fields['username'], event_id=fields['event_id']).first()
        if user:
            return Response({'ok': False, 'description': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = self.model.objects.create(username=fields['username'], event_id=fields['event_id'], password=fields['password'])
        return Response({'ok': True, 'description': 'User created'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def authenticate(self, request):
        fields = request.data
        user = self.model.objects.filter(username=fields['username'], event_id=fields['event_id']).first()
        if user:
            if user.password == fields['password']:
                return Response({'ok': True, 'description': 'Login successful', 'user_id': user.id}, status=status.HTTP_200_OK)
            return Response({'ok': False, 'description': 'Wrong password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'ok': False, 'description': 'Wrong credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'])
    def delete_all(self, request):
        users = self.model.objects.all()
        for user in users:
            user.delete()
        return Response({'ok': True, 'description': f'{len(users)} users deleted'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def load_csv(self, request):
        csv_file = request.data['csv_file']
        header = None if request.data['has_header'] else 'infer'
        data = pd.read_csv(csv_file, header=header)
        # data = data.dropna(how='all')
        for i in range(len(data)):
            row = data.iloc[i]
            user = self.model.objects.filter(username=row[0], event_id=row[2]).first()
            if not user:
                self.model.objects.create(logs=str(row), username=row[0], password=row[1], event_id=row[2])
        return Response({'ok': True}, status=status.HTTP_200_OK)