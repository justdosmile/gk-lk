from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


# class ServiceGroup(models.Model):
#     """Группы"""
#     name = models.CharField("Группа", max_length=50)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "Группа"
#         verbose_name_plural = "Группы"


class Profile(models.Model):
    """Профиль"""

    # Группа пользователя
    #     - кандидат в пайщики
    #     - пайщик
    #     - должник
    #     - распространитель первого уровня
    #     - распространитель второго уровня
    #     - распространитель третьего уровня
    #     - администратор

    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    full_name = models.CharField("ФИО", max_length=100)
    number_user = models.CharField("Личный номер пользователя", max_length=50, blank=True, null=True)
    phone = models.CharField("Телефон", max_length=12)
    email = models.EmailField("Email", max_length=50)
    passport = models.CharField("Паспорт", max_length=15)
    birthday = models.DateField("Дата рождения", max_length=8, null=True)
    citizenship = models.CharField("Гражданство", max_length=25)
    division_code = models.CharField("Код подразделения", max_length=15, blank=True, null=True)
    date_passport = models.DateField("Дата выдачи паспорта", null=True)
    inn = models.IntegerField("ИНН", blank=True, null=True)
    by_passport = models.CharField("Кем выдан", max_length=250)
    profile_region = models.CharField("Регион", max_length=50, blank=True, null=True)
    profile_city = models.CharField("Город", max_length=50, blank=True, null=True)
    schooling = models.TextField("Образование", max_length=15, blank=True, null=True)
    region_purchase = models.CharField("Регион преобритения объекта недвижимости", max_length=50)
    cost_housing = models.PositiveIntegerField("Стоимость жилья", null=True)

    date_activation = models.DateTimeField("Дата активации",
                                           help_text="Заполняется администратором",
                                           null=True,
                                           blank=True)
    accumulated_queue = models.IntegerField("Накопленно для очереди", blank=True, null=True)
    left_queue = models.IntegerField("Осталось для очереди", blank=True, null=True)
    documents = models.BooleanField("Документы да/нет", default=False, blank=True, null=True)
    number_queue = models.IntegerField("Номер очереди", blank=True, null=True)
    date_acquisition = models.DateField("Дата покупки объекта", blank=True, null=True)
    date_entry = models.DateTimeField("Дата вступления в ЖК", blank=True, null=True)
    date_joined = models.DateField("Дата активации", blank=True, null=True)
    date_repayment = models.DateField("Дата погашения", blank=True, null=True)
    installment_period = models.DateTimeField("Срок рассрочки", blank=True, null=True)
    percent_installment = models.IntegerField("Процент рассрочки", blank=True, null=True)
    number_score = models.CharField("Номер счета", max_length=15, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.user)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        permissions = [
            ("administrator", "Администратор"),
            ("candidate_in_shareholder", "Кандидат в пайщики"),
            ("shareholder", "Пайщик"),
            ("distributor_one", "Распространитель1"),
            ("distributor_two", "Распространитель2"),
            ("distributor_three", "Распространитель3"),
            ("locked", "Заблокированные"),
        ]


class AbstractAddressModel(models.Model):
    """Абстрактная модель адреса"""
    country = models.CharField("Страна", max_length=50, blank=True)
    region = models.CharField("Регион", max_length=50, blank=True)
    city = models.CharField("Город", max_length=50, blank=True)
    street = models.CharField("Улица", max_length=50, blank=True)
    house = models.IntegerField("Дом", blank=True, null=True)
    corpus = models.CharField("Корпус", max_length=50, blank=True)
    flat = models.IntegerField("Квартира", blank=True, null=True)
    index = models.IntegerField("Индекс", blank=True, null=True)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"
        abstract = True


class AddressRegistration(AbstractAddressModel):
    """Адрес регистрации"""
    reg_name = models.OneToOneField(User,
                                    verbose_name="Адрес регистрации",
                                    blank=True,
                                    on_delete=models.CASCADE)

    def __str__(self):
        return f"reg_name"

    class Meta:
        verbose_name = "Адрес регистрации"
        verbose_name_plural = "Адреса регистрации"


class AddressActual(AbstractAddressModel):
    """Адрес фактического проживания"""
    act_name = models.OneToOneField(User,
                                    verbose_name="Адрес фактического проживания",
                                    blank=True,
                                    on_delete=models.CASCADE)

    def __str__(self):
        return f"act_name"

    class Meta:
        verbose_name = "Адрес фактического проживания"
        verbose_name_plural = "Адреса фактического проживания"


class AddressPost(AbstractAddressModel):
    """Почтовый адрес для связи"""
    post_name = models.OneToOneField(User,
                                     verbose_name="Почтовый адрес для связи",
                                     blank=True,
                                     on_delete=models.CASCADE)

    def __str__(self):
        return f"post_name"

    class Meta:
        verbose_name = "Почтовый адрес для связи"
        verbose_name_plural = "Почтовые адреса для связи"


# происходит конфликт с формой регистрации
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     """Создание профиля пользователя при регистрации"""
#     if created:
#         Profile.objects.create(user=instance, id=instance.id)
#         instance.profile.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля пользователя при регистрации"""
    if created:
        AddressRegistration.objects.create(reg_name=instance, id=instance.id)
        AddressActual.objects.create(act_name=instance, id=instance.id)
        AddressPost.objects.create(post_name=instance, id=instance.id)

# 4.3. Анкета









