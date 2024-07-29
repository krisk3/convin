from . import serializers
from . import models
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes


class UserCreateView(APIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def post(self, request):
        """Create a new user"""
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
    OpenApiParameter(name='email', type=OpenApiTypes.EMAIL, description='Comma separated emails of the users.', required=False,),
    OpenApiParameter(name='mobile', type=OpenApiTypes.STR, description='Comma separated mobiles of the users.', required=False,),
],
responses={status.HTTP_200_OK: serializers.UserSerializer()})
class UserListView(APIView):
    """Retrieve users using their email or mobile number."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email', None)
        mobile = request.query_params.get('mobile', None)

        if email and mobile:
            email_list = [mail.strip() for mail in email.split(',')]
            mobile_list = [mob.strip() for mob in mobile.split(',')]
            user = models.User.objects.filter(Q(email__in=email_list) | Q(mobile__in=mobile_list))
        elif email:
            email_list = [mail.strip() for mail in email.split(',')]
            user = models.User.objects.filter(email__in=email_list)
        elif mobile:
            mobile_list = [mob.strip() for mob in mobile.split(',')]
            user = models.User.objects.filter(mobile__in=mobile_list)
        else:
            return Response({"error": "Email or mobile number must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        if user.exists():
            serializer = serializers.UserSerializer(user, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Users not found."}, status=status.HTTP_404_NOT_FOUND)