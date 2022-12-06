from django.contrib.auth.models import User                             # User Model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token                       # Token Model
from rest_framework.validators import UniqueValidator                   # 이메일 중복 방지를 위한 검증 도구
from django.contrib.auth import authenticate                            # TokenAuth 방식으로 유저를 인증해줌
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user

# ModelSerializer 안씀
class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    #write_only을 통해 클라이언트 -> 서버 방향의 역직렬화만 가능

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."}
        )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("nickname", "position", "subjects", "image")