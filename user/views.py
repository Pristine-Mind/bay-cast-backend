from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

from rest_framework import (
    views,
    response,
    status,
    viewsets,
)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .serializers import RegistrationSerializer, UserSerializer
from .filterset import UserFilter


def bad_request(message):
    return JsonResponse(
        {
            "statusCode": 400,
            "error_message": message
        },
        status=400
    )


class RegistrationView(views.APIView):

    def post(self, request, version=None):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            serializer.data, status=status.HTTP_200_OK
        )


class LoginView(views.APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        user = authenticate(username=username, password=password)
        if user is not None:
            api_key, created = Token.objects.get_or_create(user=user)

            if not created:
                api_key.created = timezone.now()
                api_key.save()

            return JsonResponse(
                {
                    "token": api_key.key,
                    "username": username,
                    "first": user.first_name,
                    "last": user.last_name,
                    "expires": api_key.created + timedelta(7),
                    "id": user.id,
                }
            )
        else:
            return bad_request("Invalid username or password")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        url_path="me",
        serializer_class=UserSerializer,
    )
    def get_authenticated_user_info(self, request, *args, **kwargs):
        return response.Response(self.get_serializer_class()(request.user).data)
