from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import authentication
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
import jwt
from jwt import decode as jwt_decode
from .serializers import UserSerializer, UserTokenObtainPairSerializer
# from users import tasks
from . import tasks
# Create your views here.

User = get_user_model()


class UserRregisterView(GenericAPIView):
    """ 
    用户使用邮箱注册
    参数：username password1 password2 email
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = [TokenAuthentication, ]

    def __email_body(self, username, absolute_url, first_msg, last_msg):
        return "您好，" + username + first_msg + "\n" + \
            absolute_url + "\n" + last_msg

    # 根据token、current_site和user生成邮件的内容
    def __email_data(self, token, current_site, user):
        relativeUrl = reverse("email_verify")
        absoluteUrl = "http://" + current_site + \
            relativeUrl + "?token=" + str(token)
        first_msg = settings.FIRST_MSG
        last_msg = settings.LAST_MSG
        email_body = self.__email_body(
            user.username, absoluteUrl, first_msg, last_msg)
        data = {"email_body": email_body, "email_subject": "验证邮箱账户",
                "to_email": user.email}
        return data

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        email_user = User.objects.filter(email=email)
        if email_user:
            return Response({"msg": "用户已存在"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = AccessToken.for_user(user)
        current_site = get_current_site(request).domain
        data = self.__email_data(token, current_site, user)
        tasks.send_email.delay(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmailVerifyView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        token = request.query_params.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if user.is_verify:
                return Response({"email": "已经验证，请勿重复验证"},
                                status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            user.is_verify = True
            user.save()
            return Response({"email": "验证成功"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            return Response({"email": "验证Token已过期"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({"email": "Token验证不合法"}, status=status.HTTP_400_BAD_REQUEST)


class LoginVerifyView(GenericAPIView):
    """
    登陆验证：email/username password
    """
    serializer_class = UserTokenObtainPairSerializer
    permission_classes = [AllowAny, ]

    def __authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(Q(email=email) | Q(username=email))
            if user.check_password(password):
                return user
            return 1
        except Exception as e:
            return None

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        user = self.__authenticate(email=email, password=password)
        if not user:
            return Response({"msg": "用户未注册或未激活账户"}, status=status.HTTP_404_NOT_FOUND)
        elif user == 1:
            return Response({"msg": "密码不正确"}, status=status.HTTP_400_BAD_REQUEST)
        refresh = self.get_serializer().get_token(user)
        return Response({
            "msg": "登陆成功",
            "username": refresh["username"],
            "token": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_200_OK)


class ResetPasswordView(GenericAPIView):
    ''' 根据邮箱、用户名重设密码，重设成功后发送邮件通知用户 '''
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        emailOrUsername = request.data['email']
        user = User.objects.filter(Q(email=emailOrUsername)
                                   | Q(username=emailOrUsername)).first()
        serializer = self.get_serializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "email_subject": "邮箱用户重设密码",
            "email_body": "密码重设成功，请登陆！",
            "to_email": user.email
        }
        tasks.send_email.delay(data)
        return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)


class GetUsersView(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication, ]
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer


user_register_view = UserRregisterView.as_view()
email_verify_view = EmailVerifyView.as_view()
login_verify_view = LoginVerifyView.as_view()
reset_password_view = ResetPasswordView.as_view()
user_list_view = GetUsersView.as_view({"get": "list"})
user_single_view = GetUsersView.as_view({
    "get": "retrieve",
    "delete": "destroy"
})
