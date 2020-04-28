from django.shortcuts import render
from django.views.generic import ListView

from .models import Profile


class Turn(ListView):
    """Очередь"""
    paginate_by = 5
    template_name = "turn/turn_list.html"

    def get_queryset(self):
        return Profile.objects.all()


class MembersCollective(ListView):
    """Члены кооператива"""
    paginate_by = 12
    template_name = "turn/members_list.html"

    def get_queryset(self):
        return Profile.objects.all()


class PartnerCollective(ListView):
    """Пайщики кооператива"""
    paginate_by = 5
    template_name = "turn/partner_list.html"

    def get_queryset(self):
        return Profile.objects.all()


class Deal(ListView):
    """В процессе сделки"""
    paginate_by = 5
    template_name = "turn/deal_list.html"

    def get_queryset(self):
        return Profile.objects.all()


class Calculated(ListView):
    """Полностью рассчитанные"""
    paginate_by = 5
    template_name = "turn/calculated_list.html"

    def get_queryset(self):
        return Profile.objects.all()


class Debtor(ListView):
    """Должники"""
    paginate_by = 5
    template_name = "turn/debtor_list.html"

    def get_queryset(self):
        return Profile.objects.all()

# 888