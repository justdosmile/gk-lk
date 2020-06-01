from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from backend.calculator.models import Calculator
from backend.profile.permissions import LockedPermissionsMixin


class CalculatorView(LockedPermissionsMixin, ListView):
    """Калькулятор"""
    model = Calculator
    template_name = "pages/calculator.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["programs"] = Calculator.objects.all()
        return context


def answer_me(request):
    summa = request.GET.get('summa')
    program = request.GET.get('programa')
    program_filter = Calculator.objects.get(percent_fee=program)
    diapazon = program_filter.parametercalculator_set.get(range_from__lte=summa, range_to__gte=summa)
    vstup_vznos = diapazon.entry_fee
    mounth_vznos = diapazon.monthly_fee
    min_payment = diapazon.min_payment
    percent_mortgage = program_filter.percent_mortgage

    return JsonResponse({'vstup_vznos': vstup_vznos, "mounth_vznos": mounth_vznos, "percent_mortgage": percent_mortgage,
                         "min_payment": min_payment})
