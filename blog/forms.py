from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    #email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
    #        'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
    #    user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            return user


#class ProfileForm(forms.Form):
#    first_name=forms.CharField(label='First Name', max_length=30)
#    last_name=forms.CharField(label='Last Name',max_length=30)
#    dob=forms.DateField(label='Date Of Birth',widget=forms.SelectDateWidget(years=[y for y in range(1930,2005)]))
#    username= forms.CharField(label='Enter Username' , min_length=4 , max_length = 50)
#    #email = forms.EmailField(label= 'Enter your email id')


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields= (
            'first_name',
            'last_name',
            'password',
        )

        
