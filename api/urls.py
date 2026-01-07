from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.endpoints import (
                           BusinessObjectViewSet,
                           MyTokenObtainPairView,
                           MyTokenRefreshView,
                           UserViewSet,
                           logout_view,
)
from api.endpoints.access import AccessRuleViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'business-objects', BusinessObjectViewSet, basename='business-object')
router.register(r'access-rules', AccessRuleViewSet, basename='access-rule')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', logout_view, name='logout'),
]
