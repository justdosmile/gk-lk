from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .forms import UpdateAddressRegistrationForm, UpdateAddressActualForm
from .models import Profile, AddressRegistration, AddressActual


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
        return Profile.objects.all()

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or user.has_perm('profile.distributor_one') or user.has_perm('profile.distributor_two') or user.has_perm('profile.distributor_three')

    def handle_no_permission(self):
        return redirect('/')

    # def has_permission(self):
    #     user = self.request.user
    #     return user.has_perm('profile.shareholder')
    #
    # def handle_no_permission(self):
    #     return redirect('/')


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


class CreateAddressView(View):
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


# -? для теста
class SupportView(LoginRequiredMixin, ListView):
    """Поддержка"""
    model = Profile
    template_name = "pages/support.html"


# -? для теста
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
    """Админка верификация пользователей"""
    model = Profile
    template_name = "administrirovanie/admin-verif.html"

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator')

    def handle_no_permission(self):
        return redirect('/')


# -? для теста
class AdminAllPaymentView(PermissionRequiredMixin, ListView):
    """Админка подтверждение платежей"""
    model = Profile
    template_name = "administrirovanie/admin-podtv.html"

    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator')

    def handle_no_permission(self):
        return redirect('/')

# # -? для теста
# class AdminAllSupportView(PermissionRequiredMixin, ListView):
#     """Админка техподдержка"""
#     model = Profile
#     template_name = "administrirovanie/admin-support.html"
#     permission_required = "profile.view_profile"

