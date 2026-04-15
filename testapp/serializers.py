from rest_framework import serializers
from .models import User, Test, Question

# ── 2. Register serializer (for creating a new user) ──────
class RegisterSerializer(serializers.ModelSerializer):
    # write_only=True → password goes IN but never comes back out
    password = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES,required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model  = User
        fields = ['username', 'email', 'password', 'role', 'first_name', 'last_name']

    def create(self, validated_data):
        # Override create() — like method overriding in OOP
        # We MUST use create_user() so password gets hashed
        return User.objects.create_user(**validated_data)


# ── 1. User serializer (read-only, for showing user info) ──
class UserSerializer(serializers.ModelSerializer):
    # ModelSerializer = inheritance from DRF base class
    # Meta inner class = tells it WHICH model and WHICH fields
    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class LoginResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'role']

class CreateTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'title', 'time_limit', 'is_published', 'created_at']
        read_only_fields = ['id', 'created_at']

class CreatQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id','test', 'text', 'question_type', 'marks']
        read_only_fields = ['id']

