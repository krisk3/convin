from . import serializers
from . import models
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

# Create your views here.
class UserCreateView(APIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['mobile'] == "":
                serializer.validated_data['mobile'] = None
            user = models.User.objects.create_user(
                email=serializer.validated_data['email'],
                name=serializer.validated_data['name'],
                password=serializer.validated_data['password'],
                mobile=serializer.validated_data.get('mobile', None)
            )
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)