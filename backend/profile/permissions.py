from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect


class AdminPermissionsMixin(PermissionRequiredMixin):
    """Разрешен доступ только администраторам"""
    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator')

    def handle_no_permission(self):
        return redirect('/')


class ShareholderPermissionsMixin(AdminPermissionsMixin):
    """Разрешен доступ только администраторам и пайщикам"""
    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or \
               user.has_perm('profile.shareholder')


class CandidateShareholderPermissionsMixin(AdminPermissionsMixin):
    """Разрешен доступ только администраторам, пайщикам и кандидатам"""
    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or \
               user.has_perm('profile.shareholder') or \
               user.has_perm('profile.candidate_in_shareholder')


class DistributorPermissionsMixin(AdminPermissionsMixin):
    """Разрешен доступ только администраторам и распространителям"""
    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or \
               user.has_perm('profile.distributor_one') or \
               user.has_perm('profile.distributor_two') or \
               user.has_perm('profile.distributor_three')


class NoAdminPermissionsMixin(AdminPermissionsMixin):
    """Разрешен доступ всем кроме администраторов"""
    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.distributor_one') or \
               user.has_perm('profile.distributor_two') or \
               user.has_perm('profile.distributor_three') or \
               user.has_perm('profile.shareholder') or \
               user.has_perm('profile.candidate_in_shareholder') or \
               user.has_perm('profile.locked')


class LockedPermissionsMixin(AdminPermissionsMixin):
    """Разрешен доступ всем кроме заблокированных"""
    def has_permission(self):
        user = self.request.user
        return user.has_perm('profile.administrator') or \
               user.has_perm('profile.distributor_one') or \
               user.has_perm('profile.distributor_two') or \
               user.has_perm('profile.distributor_three') or \
               user.has_perm('profile.shareholder') or \
               user.has_perm('profile.candidate_in_shareholder')



