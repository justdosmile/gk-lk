from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission, User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .forms import UpdateAddressRegistrationForm, UpdateAddressActualForm
from .models import Profile, AddressRegistration, AddressActual
from ..feedback.models import Feedback


class TurnView(PermissionRequiredMixin, ListView):
    """Очередь"""
    paginate_by = 10
    template_name = "turn/turn_list.html"

    def get_queryset(self):
        return Profile.objects.all()

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.distributor_one') or user.has_perm('profile.distributor_two') or user.has_perm('profile.distributor_three')

    def handle_no_permission(self):
        return redirect('/')


class MembersCollectiveView(PermissionRequiredMixin, ListView):
    """Члены кооператива"""
    paginate_by = 10
    template_name = "turn/members_list.html"
    permission_required = "profile.view_profile"

    def get_queryset(self):
        return Profile.objects.all()

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.distributor_one') or user.has_perm('profile.distributor_two') or user.has_perm('profile.distributor_three')

    def handle_no_permission(self):
        return redirect('/')


class PartnerCollectiveView(PermissionRequiredMixin, ListView):
    """Пайщики кооператива"""
    paginate_by = 10
    template_name = "turn/partner_list.html"

    def get_queryset(self):
        perm = Permission.objects.get(codename='shareholder')
        return User.objects.filter(groups__permissions=perm)

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.distributor_one') or user.has_perm('profile.distributor_two') or user.has_perm('profile.distributor_three')

    def handle_no_permission(self):
        return redirect('/')


class DealView(PermissionRequiredMixin, ListView):
    """В процессе сделки"""
    paginate_by = 10
    template_name = "turn/deal_list.html"

    def get_queryset(self):
        return Profile.objects.all()

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.distributor_one') or user.has_perm('profile.distributor_two') or user.has_perm('profile.distributor_three')

    def handle_no_permission(self):
        return redirect('/')


class CalculatedView(PermissionRequiredMixin, ListView):
    """Полностью рассчитанные"""
    paginate_by = 10
    template_name = "turn/calculated_list.html"

    def get_queryset(self):
        return Profile.objects.all()

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.distributor_one') or user.has_perm('profile.distributor_two') or user.has_perm('profile.distributor_three')

    def handle_no_permission(self):
        return redirect('/')


class DebtorView(PermissionRequiredMixin, ListView):
    """Должники"""
    paginate_by = 10
    template_name = "turn/debtor_list.html"

    def get_queryset(self):
        return Profile.objects.all()

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.distributor_one') or user.has_perm('profile.distributor_two') or user.has_perm('profile.distributor_three')

    def handle_no_permission(self):
        return redirect('/')


class ProfileView(PermissionRequiredMixin, DetailView):
    """Профиль пользователя"""
    model = Profile
    template_name = "profile/profil.html"

    def get_object(self, queryset=None):
        obj = get_object_or_404(Profile, user=self.request.user)
        return obj

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.distributor_one') or user.has_perm('profile.distributor_two') or user.has_perm('profile.distributor_three') or user.has_perm('profile.shareholder') or user.has_perm('profile.candidate_in_shareholder')

    def handle_no_permission(self):
        return redirect('/')


class CreateAddressView(PermissionRequiredMixin, View):
    """Создаем или обновляем адреса"""

    def post(self, request):
        if request.POST.get("submit_one"):
            form_1 = UpdateAddressRegistrationForm(request.POST)
            if form_1.is_valid():
                obj, created = AddressRegistration.objects.update_or_create(
                    reg_name=request.user, defaults={"country": request.POST.get('country'),
                                                     "region": request.POST.get('region'),
                                                     "city": request.POST.get('city'),
                                                     "street": request.POST.get('street'),
                                                     "house": str(request.POST.get('house')),
                                                     "corpus": request.POST.get('corpus'),
                                                     "flat": request.POST.get('flat'),
                                                     "index": request.POST.get('index'),
                                                     })
                messages.success(self.request, f'Изменения сохранены')
                return redirect('/profile/')

        if request.POST.get("submit_two"):
            form_2 = UpdateAddressActualForm(request.POST)
            if form_2.is_valid():
                obj, created = AddressActual.objects.update_or_create(
                    act_name=request.user, defaults={"country": request.POST.get('country'),
                                                     "region": request.POST.get('region'),
                                                     "city": request.POST.get('city'),
                                                     "street": request.POST.get('street'),
                                                     "house": request.POST.get('house'),
                                                     "corpus": request.POST.get('corpus'),
                                                     "flat": request.POST.get('flat'),
                                                     "index": request.POST.get('index'),
                                                     })
                messages.success(self.request, f'Изменения сохранены')
                return redirect('/profile/')

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.distributor_one') or user.has_perm('profile.distributor_two') or user.has_perm('profile.distributor_three') or user.has_perm('profile.shareholder') or user.has_perm('profile.candidate_in_shareholder')

    def handle_no_permission(self):
        return redirect('/')


# -? для теста
class VerificationDocView(PermissionRequiredMixin, ListView):
    """Документы"""
    model = Profile
    template_name = "documents/documents-verif.html"

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.shareholder') or user.has_perm('profile.candidate_in_shareholder')

    def handle_no_permission(self):
        return redirect('/')


# -? для теста
class PhotoVerificationDocView(PermissionRequiredMixin, ListView):
    """Фотоверификация"""
    model = Profile
    template_name = "documents/documents-photo.html"

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.shareholder') or user.has_perm('profile.candidate_in_shareholder')

    def handle_no_permission(self):
        return redirect('/')


# -? для теста
class DocView(PermissionRequiredMixin, ListView):
    """Документы"""
    model = Profile
    template_name = "documents/documents-docs.html"

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.shareholder') or user.has_perm('profile.candidate_in_shareholder')

    def handle_no_permission(self):
        return redirect('/')


# -? для теста
class SampleDocView(PermissionRequiredMixin, ListView):
    """Шаблоны и образцы"""
    model = Profile
    template_name = "documents/documents-shablon.html"

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.shareholder') or user.has_perm('profile.candidate_in_shareholder')

    def handle_no_permission(self):
        return redirect('/')


# -? для теста
class InstructionView(PermissionRequiredMixin, ListView):
    """Инструкции"""
    model = Profile
    template_name = "documents/documents-instructions.html"

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.shareholder') or user.has_perm('profile.candidate_in_shareholder')

    def handle_no_permission(self):
        return redirect('/')


# -? для теста
class EntranceFeeView(PermissionRequiredMixin, ListView):
    """Вступительный взнос"""
    model = Profile
    template_name = "vznos/vznos-vznos_vstup.html"

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.shareholder')

    def handle_no_permission(self):
        return redirect('/')


# -? для теста
class SharePremiumView(PermissionRequiredMixin, ListView):
    """Паевый взнос"""
    model = Profile
    template_name = "vznos/vznos-vznos_paev.html"

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.shareholder')

    def handle_no_permission(self):
        return redirect('/')


# -? для теста
class ConfirmPaymentView(PermissionRequiredMixin, ListView):
    """Подтвердить взнос"""
    model = Profile
    template_name = "vznos/vznos-vznos_podtv.html"

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.shareholder')

    def handle_no_permission(self):
        return redirect('/')


# -? для теста
class HistoryPaymentView(PermissionRequiredMixin, ListView):
    """История платежей"""
    model = Profile
    template_name = "vznos/vznos-myvznos.html"

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.shareholder')

    def handle_no_permission(self):
        return redirect('/')


# -? для теста
class HierarchyView(PermissionRequiredMixin, ListView):
    """Иерархия приглашений"""
    model = Profile
    template_name = "distribution/ierarhiya.html"

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.distributor_one') or user.has_perm('profile.distributor_two') or user.has_perm('profile.distributor_three')

    def handle_no_permission(self):
        return redirect('/')


# -? для теста
class LinkInvitationView(PermissionRequiredMixin, ListView):
    """Ссылки для приглашения"""
    model = Profile
    template_name = "distribution/raspr-links.html"

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.distributor_one') or user.has_perm('profile.distributor_two') or user.has_perm('profile.distributor_three')

    def handle_no_permission(self):
        return redirect('/')


# # -? для теста
# class SupportView(LoginRequiredMixin, ListView):
#     """Поддержка"""
#     model = Profile
#     template_name = "pages/support.html"


class AdminAllUserView(PermissionRequiredMixin, ListView):
    """Админка все пользователи"""
    model = Profile
    template_name = "administrirovanie/admin-allusers.html"

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator')

    def handle_no_permission(self):
        return redirect('/')


# -? для теста
class AdminAllVerificationView(PermissionRequiredMixin, ListView):
    """Админка ожидающие верификацию пользователи"""
    template_name = "administrirovanie/admin-verif.html"

    def get_queryset(self):
        perm = Permission.objects.get(codename='candidate_in_shareholder')
        return User.objects.filter(groups__permissions=perm)

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator')

    def handle_no_permission(self):
        return redirect('/')


# -? для теста
class AdminAllPaymentView(PermissionRequiredMixin, ListView):
    """Админка подтверждение платежей"""
    template_name = "administrirovanie/admin-podtv.html"

    def get_queryset(self):
        perm = Permission.objects.get(codename='shareholder')
        return User.objects.filter(groups__permissions=perm)

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator')

    def handle_no_permission(self):
        return redirect('/')


# надо поработать над пагинатором но это не точно)
class SearchAdminView(PermissionRequiredMixin, View):
    """Админка Поиск пользователей по ФИО """

    def get(self, request):
        if self.request.GET.get('all'):
            all_users = {'object_list': Profile.objects.filter(full_name__icontains=self.request.GET.get('all'))}
            return render(self.request, 'administrirovanie/admin-allusers.html', all_users)
        elif self.request.GET.get('verif'):
            verification = {'object_list': User.objects.filter(groups__permissions=Permission.objects.get(codename='candidate_in_shareholder'), profile__full_name__icontains=self.request.GET.get('verif'))}
            return render(self.request, 'administrirovanie/admin-verif.html', verification)
        elif self.request.GET.get('podtv'):
            paying = {'object_list': User.objects.filter(groups__permissions=Permission.objects.get(codename='shareholder'), profile__full_name__icontains=self.request.GET.get('podtv'))}
            return render(self.request, 'administrirovanie/admin-podtv.html', paying)
        elif self.request.GET.get('qus'):
            support = {'object_list': Feedback.objects.filter(user__profile__full_name__icontains=self.request.GET.get('qus'))}
            return render(self.request, 'administrirovanie/admin-support.html', support)

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator')

    def handle_no_permission(self):
        return redirect('/')


# надо поработать над пагинатором но это не точно)
class SearchTurnView(PermissionRequiredMixin, View):
    """Очередь Поиск пользователей по ФИО"""

    def get(self, request):
        if self.request.GET.get('turn'):
            turn = {'object_list': Profile.objects.filter(full_name__icontains=self.request.GET.get('turn'))}
            return render(self.request, "turn/turn_list.html", turn)
        elif self.request.GET.get('partner'):
            partner = {'object_list': User.objects.filter(groups__permissions=Permission.objects.get(codename='shareholder'), profile__full_name__icontains=self.request.GET.get('partner'))}
            return render(self.request, "turn/partner_list.html", partner)
        elif self.request.GET.get('member'):
            member = {'object_list': Profile.objects.filter(full_name__icontains=self.request.GET.get('member'))}
            return render(self.request, "turn/members_list.html", member)
        elif self.request.GET.get('debtor'):
            debtor = {'object_list': Profile.objects.filter(full_name__icontains=self.request.GET.get('debtor'))}
            return render(self.request, "turn/debtor_list.html", debtor)
        elif self.request.GET.get('deal'):
            deal = {'object_list': Profile.objects.filter(full_name__icontains=self.request.GET.get('deal'))}
            return render(self.request, "turn/deal_list.html", deal)
        elif self.request.GET.get('calc'):
            calc = {'object_list': Profile.objects.filter(full_name__icontains=self.request.GET.get('calc'))}
            return render(self.request, "turn/calculated_list.html", calc)

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.distributor_one') or user.has_perm('profile.distributor_two') or user.has_perm('profile.distributor_three')

    def handle_no_permission(self):
        return redirect('/')

