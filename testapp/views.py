from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .permissions import IsTeacher
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, LoginResponseSerializer, CreateTestSerializer, CreatQuestionSerializer
from django.contrib.auth import authenticate

# ── Helper: generate tokens for a user ────────────────────
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access':  str(refresh.access_token),
    }

# Create your views here.
# ══════════════════════════════════════════════════════════
# REGISTER VIEW
# ══════════════════════════════════════════════════════════
class RegisterView(APIView):
    # AllowAny — no token needed to register (makes sense!)
    permission_classes = [AllowAny]

    def post(self, request):
        # 1. Pass incoming JSON to serializer
        serializer = RegisterSerializer(data=request.data)

        # 2. Validate — like our __init__ type checks in OOP
        if serializer.is_valid():
            # 3. Save → calls our overridden create() → create_user()
            user = serializer.save()

            # 4. Generate JWT tokens
            tokens = get_tokens_for_user(user)

            # 5. Return user data + tokens
            return Response({
                'user':   UserSerializer(user).data,
                'tokens': tokens,
            }, status=status.HTTP_201_CREATED)

        # Validation failed → return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def home(request):
        return render(request, 'index.html')

# ══════════════════════════════════════════════════════════
# LOGIN VIEW
# ══════════════════════════════════════════════════════════
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        if not login_serializer.is_valid():
            return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = login_serializer.validated_data['username']  
        password = login_serializer.validated_data['password']
        # Django's built-in authenticate checks username + password
        user = authenticate(username=username, password=password)

        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response({
                'user':   LoginResponseSerializer(user).data,
                'tokens': tokens,
            })

        return Response(
            {'error': 'Invalid username or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
class CreateTestView(APIView):
    permission_classes = [IsTeacher]   # user must be logged in

    def post(self, request):
        serializer = CreateTestSerializer(data=request.data)

        if serializer.is_valid():
            # Automatically assign logged-in user
            test = serializer.save(created_by=request.user)

            return Response({
                "message": "Test created successfully",
                "test_id": test.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class CreateQuestionView(APIView):
    permission_classes = [IsTeacher]

    def post(self, request):
        serializer = CreatQuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save(created_by=request.user)

            return Response({
                "message": "Questions created Successfully",
                "Question_id":question.id
            }, status = status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)