from django.contrib import admin

from backend.document.models import Document, UserDocument


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Документы"""
    list_display = ('title', 'sample', 'id')
    list_display_links = ('title',)


@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'document', 'data', 'moderation', 'updated')
    list_filter = ('moderation', 'data')
    search_fields = ('users', 'user_document')