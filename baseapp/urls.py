# baseapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlatformViewSet, EntregaViewSet, RecogidaViewSet, GastoViewSet, ProfileViewSet, register_user, UserViewSet, activate_user_view
from . import views


router = DefaultRouter()
router.register(r'plataformas', PlatformViewSet, basename='plataformas')
router.register(r'entregas', EntregaViewSet, basename='entregas')
router.register(r'recogidas', RecogidaViewSet, basename='recogidas')
router.register(r'gastos', GastoViewSet, basename='gastos')
router.register(r'perfil', ProfileViewSet, basename='perfil')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('me/', views.me_view),
    path('me/update_user/', views.update_user_view),
    path('factura/', views.generar_factura_pdf),
    path('register/', register_user, name='register'),
    path('activate_user/<int:pk>/', activate_user_view, name='activate_user'),
]
