from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Document(models.Model):
    """Документы"""
    STATUS_CHOICES = (
        ('document', 'Документы'),
        ('photo_verification', 'Фотоверификация'),
        ('templates_and_samples', 'Шаблоны и образцы'),
        ('instructions', 'Инструкции'),
    )

    title = models.CharField("Документ", max_length=150)
    sample = models.FileField("Образец", upload_to='document')
    document = models.CharField('Статус документа', max_length=21, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"


class UserDocument(models.Model):
    """Загрузка документов"""
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    document = models.ForeignKey(Document, verbose_name="Документ", on_delete=models.CASCADE, related_name='docs')
    user_document = models.FileField("Документ", upload_to='user_document')
    data = models.DateTimeField("Дата загрузки", auto_now_add=True, null=True)
    updated = models.DateTimeField('Дата проверки', auto_now=True)
    moderation = models.BooleanField("Проверен", default=False)

    def __str__(self):
        return "{}".format(self.user)

    class Meta:
        verbose_name = "Документ пользователя"
        verbose_name_plural = "Документы пользователей"
        # ordering = ('-data',)