import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


# def get_path_img_feedback(instanse, file):
#
#     end_extention = file.split('.')[-1]
#     head = file.split('.')[0]
#     if len(head) > 10:
#         head = head[:10]
#     file_name = head + '.' + end_extention
#     return os.path.join('feedback', 'img_{}').format(file_name)


class Feedback(models.Model):
    """Модель обратной связи"""
    user = models.ForeignKey(User, verbose_name="Кто отправил", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField("Заголовок", max_length=50)
    text = models.TextField("Содержание вопроса", max_length=1000)
    image = models.ImageField("Фото/Скриншот", upload_to='feedback')
    date = models.DateTimeField("Дата добавления", auto_now_add=True, null=True)
    processing = models.BooleanField("Обработано?", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("feedback:feedback_single", kwargs={"pk": self.id})

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
        # send_mail_feedback(self.user.profile.full_name)

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратные связи"
        ordering = ["-id"]


class Answer(models.Model):
    """Ответ на вопрос"""
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, verbose_name="Вопрос", on_delete=models.CASCADE, related_name='reply')
    title = models.CharField("Заголовок", max_length=50)
    text = models.TextField("Ответ", max_length=1000)
    image = models.ImageField("Фото/Скриншот", upload_to='feedback', blank=True)
    data = models.DateTimeField("Дата написания", auto_now_add=True, null=True)

    def __str__(self):
        return "{}".format(self.user)

    class Meta:
        verbose_name = "Ответ на вопрос"
        verbose_name_plural = "Ответ на вопросы"
        # ordering = ('-data',)


@receiver(post_save, sender=Answer)
def change_processing(instance, **kwargs):
    """При создании ответа меняем processing на True"""
    profile = instance.feedback
    profile.processing = True
    profile.save()


# @receiver(post_save, sender=Feedback)
# def create_user_mess(sender, instance, created, **kwargs):
#     """Отправка сообщения на обратной связи на email"""
#     if created:
#         send_mail_feedback(instance.user)
