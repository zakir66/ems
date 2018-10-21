from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ModelChoiceField(queryset=Group.objects.all())

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password'
        ]

        label = {
            'password': 'password'
        }

        # def clean_email(self):
        #     if self.cleaned_data['email'].endswith('@aaravtech.com')
        #         return self.cleaned_data['email']
        #     else:
        #         raise ValidationError("Email id is not valid")
#...............role................
    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})

            if kwargs['instance'].groups.all():
                initial['role'] = kwargs['instance'].groups.all()[0]
            else:
                initial['role'] = None

        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self):
        password = self.cleaned_data.pop('password')
        role = self.cleaned_data.pop('role') #role er jonno
        u = super().save()
        u.groups.set([role]) #role er jonno
        u.set_password(password)
        u.save()
        return u