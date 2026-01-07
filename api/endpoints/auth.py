from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    """Вью для получения пары токенов."""
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class MyTokenRefreshView(TokenRefreshView):
    """Вью для обновления access токена по refresh."""
    permission_classes = [AllowAny]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Логаут: добавляем refresh токен в blacklist.
    Клиент должен передать refresh токен в теле запроса.
    """
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response(
            {'detail': 'Требуется refresh токен.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()  # токен теперь заблокирован
    except Exception:
        return Response(
            {'detail': 'Неверный refresh токен.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response({'detail': 'Успешный логаут.'}, status=status.HTTP_204_NO_CONTENT)
