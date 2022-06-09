from django.contrib import admin

from backend.apps.authenticator.models import PC2User

@admin.register(PC2User)
class PC2UserAdmin(admin.ModelAdmin):
    list_display=('id', 'username', 'event_id', 'archived')
    list_filter=('archived',)
