from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, UserDetailsViewSet, api_root, create_user, get_all_users, login_user, create_transaction

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'users', UserDetailsViewSet, basename='userdetails')

urlpatterns = [
    path('', api_root, name='api-root'),
    path('', include(router.urls)),
    path('v1/create_user/', create_user, name='create-user'),
    path('v1/get_all_users/', get_all_users, name='get-all-users'),
    path('v1/login/', login_user, name='login_user'),
    path('v1/create_transaction/', create_transaction, name='create-transaction'),
] 