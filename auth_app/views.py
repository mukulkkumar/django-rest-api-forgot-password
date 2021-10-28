from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_pass_proj.settings import EMAIL_HOST_USER

from django.contrib.auth.models import User
from .serializers import (
    SendVerificationLinkSerializer, 
    ChangePasswordSerializer
)

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.
class SendEmailView(APIView):
    http_method_names = ['post']

    def post(self, request, format=None):

        serializer = SendVerificationLinkSerializer(data=request.data)
        
        if serializer.is_valid():
            email_address = serializer.validated_data.get('email_address')

            # check whether the user exist in our database table `auth_user` or not
            try:
                user = User.objects.get(email=email_address)
            except User.DoesNotExist:
                return Response({"msg": "Invalid Email"}, status=status.HTTP_412_PRECONDITION_FAILED)

            # Generate verification link
            domain = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            password_reset_token_generator = PasswordResetTokenGenerator()
            token = password_reset_token_generator.make_token(user)

            data_for_email = {
                "domain": str(domain),
                "uid": uid,
                "token": token,
                "username": user.username,
                "user_email_data": {
                    "user_full_name": user.first_name + " " + user.last_name
                },
            }

            # Send an email
            subject = "Forgot Password"
            message = render_to_string('forgot_password_email.html', data_for_email)
            recepient = email_address
            email = EmailMessage(subject=subject, body=message, from_email=EMAIL_HOST_USER, to=[email_address])
            email.content_subtype = "html"

            try:
                email.send(fail_silently=False)
                return Response({'msg': 'Email sent successfully.'}, status=status.HTTP_200_OK)
            except Exception as ex:
                return Response({'msg': 'Email is not sent to the user'}, status=status.HTTP_412_PRECONDITION_FAILED)

        return Response({'msg': 'Invalid request'}, status=status.HTTP_412_PRECONDITION_FAILED)


class UserEmailLinkView(APIView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):

        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')

        uid = force_text(urlsafe_base64_decode(uidb64))

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({"msg": "Invalid Link"}, status=status.HTTP_412_PRECONDITION_FAILED)

        account_activation_token = PasswordResetTokenGenerator()

        if user is not None and account_activation_token.check_token(user, token):
            return Response({"msg": "Valid link for password reset", "username": user.username}, status=status.HTTP_200_OK)

        return Response({"msg": "Invalid Link"}, status=status.HTTP_412_PRECONDITION_FAILED)


class ResetPasswordView(APIView):
    http_method_names = ['post']

    def post(self, request, format=None):

        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"msg": "Invalid User"}, status=status.HTTP_412_PRECONDITION_FAILED)

            if user:
                user.set_password(password)
                user.save()

                return Response({'msg': 'Password changed successfully.'}, status=status.HTTP_200_OK)

        return Response({'msg': 'Password change failure'}, status=status.HTTP_412_PRECONDITION_FAILED)

