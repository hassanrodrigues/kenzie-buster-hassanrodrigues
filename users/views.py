from .serializers import UserSerializer, CustomJWTSerializer
from .models import User
from .permissions import PermissionsPersonalized
from rest_framework.views import APIView, Response, Request, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class LoginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer


class UserView(APIView):
    def get(self, req: Request) -> Response:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, req: Request) -> Response:
        user = UserSerializer(data=req.data)
        user.is_valid(raise_exception=True)
        user.save()

        return Response(user.data, status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [PermissionsPersonalized, IsAuthenticated]

    def get(self, req: Request, user_id: int) -> Response:
        user = User.objects.get(id=user_id)
        self.check_object_permissions(req, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
