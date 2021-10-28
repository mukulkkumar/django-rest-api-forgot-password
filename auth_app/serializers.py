from rest_framework import serializers

class SendVerificationLinkSerializer(serializers.Serializer):
    email_address = serializers.CharField(required=True)

class ChangePasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
