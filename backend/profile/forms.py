from django import forms

from backend.profile.models import Profile, AddressRegistration, AddressActual


class UserSignUpForm(forms.ModelForm):
    """Форма регистрации"""

    class Meta:
        model = Profile
        fields = ('full_name', 'email', 'birthday', 'date_passport', 'phone', 'by_passport',
                  'citizenship', 'passport', 'region_purchase', 'cost_housing')

    def signup(self, request, user):
        # user.username = self.cleaned_data['full_name']
        profile = Profile(user=user)
        profile.full_name = self.cleaned_data.get('full_name')
        profile.citizenship = self.cleaned_data.get('citizenship')
        profile.birthday = self.cleaned_data.get('birthday')
        profile.phone = self.cleaned_data.get('phone')
        profile.email = self.cleaned_data.get('email')
        profile.passport = self.cleaned_data.get('passport')
        profile.by_passport = self.cleaned_data.get('by_passport')
        profile.date_passport = self.cleaned_data.get('date_passport')
        profile.region_purchase = self.cleaned_data.get('region_purchase')
        profile.cost_housing = self.cleaned_data.get('cost_housing')
        #         print(profile)
        profile.save()
        # user.save()


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name']


class UpdateAddressRegistrationForm(forms.ModelForm):
    class Meta:
        model = AddressRegistration
        fields = ['country', 'region', 'city', 'street', 'house', 'corpus', 'flat', 'index']


class UpdateAddressActualForm(forms.ModelForm):
    class Meta:
        model = AddressActual
        fields = ['country', 'region', 'city', 'street', 'house', 'corpus', 'flat', 'index']

