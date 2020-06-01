from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission, User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.base import View

from .forms import UpdateAddressRegistrationForm, UpdateAddressActualForm, UpdateProfileForm
from .models import Profile, AddressRegistration, AddressActual
from .permissions import AdminPermissionsMixin, ShareholderPermissionsMixin, \
    DistributorPermissionsMixin, LockedPermissionsMixin, CandidateShareholderPermissionsMixin
from ..document.models import Document
from ..feedback.models import Feedback


class TurnView(DistributorPermissionsMixin, ListView):
    """Очередь"""
    paginate_by = 10
    template_name = "turn/turn_list.html"

    def get_queryset(self):
        return Profile.objects.all()


class MembersCollectiveView(DistributorPermissionsMixin, ListView):
    """Члены кооператива"""
    paginate_by = 10
    template_name = "turn/members_list.html"
    permission_required = "profile.view_profile"

    def get_queryset(self):
        return Profile.objects.all()


class PartnerCollectiveView(DistributorPermissionsMixin, ListView):
    """Пайщики кооператива"""
    paginate_by = 10
    template_name = "turn/partner_list.html"

    def get_queryset(self):
        perm = Permission.objects.get(codename='shareholder')
        return User.objects.filter(groups__permissions=perm)


class DealView(DistributorPermissionsMixin, ListView):
    """В процессе сделки"""
    paginate_by = 10
    template_name = "turn/deal_list.html"

    def get_queryset(self):
        return Profile.objects.all()


class CalculatedView(DistributorPermissionsMixin, ListView):
    """Полностью рассчитанные"""
    paginate_by = 10
    template_name = "turn/calculated_list.html"

    def get_queryset(self):
        return Profile.objects.all()


class DebtorView(DistributorPermissionsMixin, ListView):
    """Должники"""
    paginate_by = 10
    template_name = "turn/debtor_list.html"

    def get_queryset(self):
        return Profile.objects.all()


class ProfileView(LockedPermissionsMixin, DetailView):
    """Профиль пользователя"""
    model = Profile
    template_name = "profile/profil.html"

    def get_object(self, queryset=None):
        obj = get_object_or_404(Profile, user=self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        context['address_registration'] = AddressRegistration.objects.filter(reg_name=self.request.user)
        context['address_actual'] = AddressActual.objects.filter(act_name=self.request.user)
        return context


# class CreateAddressView(LockedPermissionsMixin, View):
#     """Создаем или обновляем адреса"""
#
#     def post(self, request):
#         if request.POST.get("submit_one"):
#             form_1 = UpdateAddressRegistrationForm(request.POST)
#             if form_1.is_valid():
#                 obj, created = AddressRegistration.objects.update_or_create(
#                     reg_name=request.user, defaults={"country": request.POST.get('country'),
#                                                      "region": request.POST.get('region'),
#                                                      "city": request.POST.get('city'),
#                                                      "street": request.POST.get('street'),
#                                                      "house": str(request.POST.get('house')),
#                                                      "corpus": request.POST.get('corpus'),
#                                                      "flat": request.POST.get('flat'),
#                                                      "index": request.POST.get('index'),
#                                                      })
#                 messages.success(self.request, f'Изменения сохранены')
#                 return redirect('/profile/')
#
#         if request.POST.get("submit_two"):
#             form_2 = UpdateAddressActualForm(request.POST)
#             if form_2.is_valid():
#                 obj, created = AddressActual.objects.update_or_create(
#                     act_name=request.user, defaults={"country": request.POST.get('country'),
#                                                      "region": request.POST.get('region'),
#                                                      "city": request.POST.get('city'),
#                                                      "street": request.POST.get('street'),
#                                                      "house": request.POST.get('house'),
#                                                      "corpus": request.POST.get('corpus'),
#                                                      "flat": request.POST.get('flat'),
#                                                      "index": request.POST.get('index'),
#                                                      })
#                 messages.success(self.request, f'Изменения сохранены')
#                 return redirect('/profile/')

class AdminUserProfileView(AdminPermissionsMixin, DetailView):
    """Администратор просмотр профиля пользователя
    необходимость данной вью, так как необходимо разграничить доступ"""
    model = Profile
    template_name = "profile/profil.html"

    def get_context_data(self, **kwargs):
        context = super(AdminUserProfileView, self).get_context_data()
        context['address_registration'] = AddressRegistration.objects.filter(reg_name__profile=self.kwargs.get('pk'))
        context['address_actual'] = AddressActual.objects.filter(act_name__profile=self.kwargs.get('pk'))
        return context


class UpdateProfileView(LockedPermissionsMixin, View):
    """Редактирование профиля пользователя"""

    def post(self, request, pk):
        if request.POST.get("submit_profile"):
            user = User.objects.get(profile=pk)
            obj = get_object_or_404(Profile, id=user.profile.id)
            form = UpdateProfileForm(self.request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return redirect(request.META.get('HTTP_REFERER'))

        if request.POST.get("submit_one"):
            user = User.objects.get(profile=pk)
            obj_1 = get_object_or_404(AddressRegistration, id=user.addressregistration.id)
            form_one = UpdateAddressRegistrationForm(self.request.POST, instance=obj_1)
            if form_one.is_valid():
                form_one.save()
                return redirect(request.META.get('HTTP_REFERER'))

        if request.POST.get("submit_two"):
            user = User.objects.get(profile=pk)
            obj_2 = get_object_or_404(AddressActual, id=user.addressactual.id)
            form_two = UpdateAddressActualForm(self.request.POST, instance=obj_2)
            if form_two.is_valid():
                form_two.save()
                return redirect(request.META.get('HTTP_REFERER'))


# -? для теста
class EntranceFeeView(ShareholderPermissionsMixin, ListView):
    """Вступительный взнос"""
    model = Profile
    template_name = "vznos/vznos-vznos_vstup.html"


# -? для теста
class SharePremiumView(ShareholderPermissionsMixin, ListView):
    """Паевый взнос"""
    model = Profile
    template_name = "vznos/vznos-vznos_paev.html"


# -? для теста
class ConfirmPaymentView(ShareholderPermissionsMixin, ListView):
    """Подтвердить взнос"""
    model = Profile
    template_name = "vznos/vznos-vznos_podtv.html"


# -? для теста
class HistoryPaymentView(ShareholderPermissionsMixin, ListView):
    """История платежей"""
    model = Profile
    template_name = "vznos/vznos-myvznos.html"


# -? для теста
class HierarchyView(DistributorPermissionsMixin, ListView):
    """Иерархия приглашений"""
    model = Profile
    template_name = "distribution/ierarhiya.html"


# -? для теста
class LinkInvitationView(DistributorPermissionsMixin, ListView):
    """Ссылки для приглашения"""
    model = Profile
    template_name = "distribution/raspr-links.html"


class AdminAllUserView(AdminPermissionsMixin, ListView):
    """Админка все пользователи"""
    model = Profile
    template_name = "administrirovanie/admin-allusers.html"


# -? для теста
class AdminAllVerificationView(AdminPermissionsMixin, ListView):
    """Админка ожидающие верификацию пользователи"""
    template_name = "administrirovanie/admin-verif.html"

    def get_queryset(self):
        perm = Permission.objects.get(codename='candidate_in_shareholder')
        return User.objects.filter(groups__permissions=perm)


class AdminAllPaymentView(AdminPermissionsMixin, ListView):
    """Админка подтверждение платежей"""
    template_name = "administrirovanie/admin-podtv.html"

    def get_queryset(self):
        perm = Permission.objects.get(codename='shareholder')
        return User.objects.filter(groups__permissions=perm)


# надо поработать над пагинатором но это не точно)
class SearchAdminView(AdminPermissionsMixin, View):
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


# надо поработать над пагинатором но это не точно)
class SearchTurnView(DistributorPermissionsMixin, View):
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


