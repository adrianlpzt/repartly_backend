# baseapp/views.py
from rest_framework import viewsets, permissions, status
from .models import Platform, Entrega, Recogida, Gasto, Profile
from .serializers import UserSerializer, UserRegisterSerializer, PlatformSerializer, EntregaSerializer, RecogidaSerializer, GastoSerializer, ProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from weasyprint import HTML
from collections import defaultdict
import os
from datetime import datetime
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from decimal import Decimal



class PlatformViewSet(viewsets.ModelViewSet):
    serializer_class = PlatformSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Platform.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EntregaViewSet(viewsets.ModelViewSet):
    serializer_class = EntregaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Entrega.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecogidaViewSet(viewsets.ModelViewSet):
    serializer_class = RecogidaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Recogida.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GastoViewSet(viewsets.ModelViewSet):
    serializer_class = GastoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Gasto.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user
    profile = user.profile
    plataformas = user.platforms.all()
    entregas = Entrega.objects.filter(user=user)
    recogidas = Recogida.objects.filter(user=user)
    gastos = Gasto.objects.filter(user=user)
    
    return Response({
        'user': UserSerializer(user).data,
        'profile': ProfileSerializer(profile).data,
        'plataformas': PlatformSerializer(plataformas, many=True).data,
        'entregas': EntregaSerializer(entregas, many=True).data,
        'recogidas': RecogidaSerializer(recogidas, many=True).data,
        'gastos': GastoSerializer(gastos, many=True).data
    })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_view(request):
    user = request.user
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.save()
    return Response(UserSerializer(user).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generar_factura_pdf(request):
    user = request.user
    mes = request.GET.get('mes')  # Formato: '2024-05'

    # Obtener datos
    entregas = Entrega.objects.filter(user=user, fecha__startswith=mes)
    recogidas = Recogida.objects.filter(user=user, fecha__startswith=mes)
    gastos = Gasto.objects.filter(user=user, fecha__startswith=mes)


    # Agrupar por plataforma
    def agrupar_por_plataforma(queryset):
        resumen = defaultdict(lambda: {"cantidad": 0, "total": Decimal("0.00")})
        for obj in queryset:
            plataforma = obj.plataforma
            resumen[plataforma]["cantidad"] += obj.cantidad
            resumen[plataforma]["total"] += Decimal(obj.total)
        return list(resumen.items())

    entregas_por_plataforma = agrupar_por_plataforma(entregas)
    recogidas_por_plataforma = agrupar_por_plataforma(recogidas)


    # Totales y cálculo de IVA
    total_entregas = sum(Decimal(e.total) for e in entregas)
    total_recogidas = sum(Decimal(r.total) for r in recogidas)
    total_gastos = sum(Decimal(g.cantidad) for g in gastos)

    subtotal = total_entregas + total_recogidas
    iva = subtotal * Decimal('0.21')
    total_con_iva = subtotal + iva
    beneficio = subtotal - total_gastos

    # Ruta del logo Repartly
    logo_path = os.path.join(settings.BASE_DIR, 'baseapp', 'static', 'images', 'repartly-logo.png')
    
    # Render HTML
    html_string = render_to_string('factura_template.html', {
        'usuario': user,
        'mes': mes,
        'entregas_por_plataforma': entregas_por_plataforma,
        'recogidas_por_plataforma': recogidas_por_plataforma,
        'total_entregas': total_entregas,
        'total_recogidas': total_recogidas,
        'total_gastos': total_gastos,
        'subtotal': subtotal,
        'iva': iva,
        'total_con_iva': total_con_iva,
        'beneficio': beneficio,
        'fecha_generacion': datetime.now(),
        'logo_path': f"file:///{logo_path.replace(os.sep, '/')}"

    })

    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="repartly_factura_{mes}.pdf"'
    return response

@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Usuario registrado correctamente. En espera de activación.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)