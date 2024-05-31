from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Account, Contact
from django.forms import ModelForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Account
        fields = ('username', 'email', 'name', 'password1', 'password2')
        
class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Account
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid username or password")
            
class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "mobile_no", "relation"]
        widgets = {
            "relation": forms.Select(choices=Contact.RELATION_CHOICES, attrs={"class": "form-control"}),
        }
