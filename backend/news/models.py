import os

from django.db import models
from django.urls import reverse
from django.utils import timezone

from backend.news.gen_slug import gen_slug


def get_path_img(instanse, file):

    end_extention = file.split('.')[-1]
    head = file.split('.')[0]
    if len(head) > 10:
        head = head[:10]
    file_name = head + '.' + end_extention
    return os.path.join('news', 'news_{}').format(file_name)


class Post(models.Model):
    """Класс модели новости"""
    title = models.CharField("Тема", max_length=500)
    mini_text = models.TextField("Краткое содержание", max_length=5000)
    text = models.TextField("Полное содержание", max_length=10000)
    created_date = models.DateField("Дата создания", auto_now_add=True)
    published_date = models.DateField("Дата публикации", blank=True, null=True)
    image = models.ImageField("Изображение", upload_to=get_path_img, blank=True)
    published = models.BooleanField("Опубликовать?", default=True)
    viewed = models.IntegerField("Просмотрено", default=0)
    slug = models.SlugField(max_length=500, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-id"]

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("single_post", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        # при создании новости в шаблоне создаем slug
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
