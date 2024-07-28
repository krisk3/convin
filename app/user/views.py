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


@extend_schema(
parameters=[
    OpenApiParameter(name='email', type=OpenApiTypes.EMAIL, description='Email of the user.', required=False,),
    OpenApiParameter(name='mobile', type=OpenApiTypes.STR, description='Mobile of the user.', required=False,),
],
responses={status.HTTP_200_OK: serializers.UserSerializer()})
class UserListView(APIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email', None)
        mobile = request.query_params.get('mobile', None)

        if email:
            user = models.User.objects.filter(email=email).first()
        elif mobile:
            user = models.User.objects.filter(mobile=mobile).first()
        elif email and mobile:
            user = models.User.objects.filter(email=email, mobile=mobile).first()
        else:
            return Response({"error": "Email or mobile number must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        if user:
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
