from django.contrib import admin

from .models import Profile, AddressRegistration, AddressActual, AddressPost


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Профиль пользователя"""
    list_display = ('user', 'id')
    list_display_links = ('user',)


@admin.register(AddressRegistration)
class AddressRegistrationAdmin(admin.ModelAdmin):
    """Адрес регистрации"""
    list_display = ('id', 'reg_name')
    list_display_links = ('reg_name',)


@admin.register(AddressActual)
class AddressActualAdmin(admin.ModelAdmin):
    """Адрес фактического проживания"""
    list_display = ('id', 'act_name')
    list_display_links = ('act_name',)


@admin.register(AddressPost)
class AddressPostAdmin(admin.ModelAdmin):
    """Почтовый адрес для связи"""
    list_display = ('id', 'post_name')
    list_display_links = ('post_name',)
