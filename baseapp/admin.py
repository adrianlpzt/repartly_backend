from django.contrib import admin
from .models import Profile, Platform, Entrega, Recogida, Gasto

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono', 'is_premium', 'fecha_registro')
    search_fields = ('user__username', 'telefono')
    list_filter = ('is_premium',)

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'user', 'precio_entrega', 'precio_recogida')
    search_fields = ('nombre', 'user__username')

@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ('user', 'plataforma', 'cantidad', 'fecha', 'total')
    list_filter = ('fecha', 'plataforma')
    search_fields = ('user__username', 'plataforma__nombre', 'observaciones')

@admin.register(Recogida)
class RecogidaAdmin(admin.ModelAdmin):
    list_display = ('user', 'plataforma', 'cantidad', 'fecha', 'total')
    list_filter = ('fecha', 'plataforma')
    search_fields = ('user__username', 'plataforma__nombre', 'observaciones')

@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ('user', 'concepto', 'cantidad', 'fecha')
    list_filter = ('fecha', 'concepto')
    search_fields = ('user__username', 'concepto', 'observaciones')
