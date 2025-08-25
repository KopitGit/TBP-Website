# Fichier: accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    nom_entreprise = forms.CharField(max_length=255, label="Nom de l'entreprise")
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmation du mot de passe")
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        
        return cleaned_data

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6, label="Code OTP")

class CustomAuthenticationForm(AuthenticationForm):
    id_entreprise = forms.CharField(max_length=8, label="ID Entreprise")
    
    def clean(self):
        id_entreprise = self.cleaned_data.get('id_entreprise')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if id_entreprise and username and password:
            try:
                # Vérifier que l'utilisateur appartient à cette entreprise
                user = User.objects.get(username=username)
                if user.profile.entreprise.id_entreprise != id_entreprise:
                    raise forms.ValidationError("Cet utilisateur n'appartient pas à cette entreprise.")
            except User.DoesNotExist:
                raise forms.ValidationError("Identifiants incorrects.")
            except Profile.DoesNotExist:
                raise forms.ValidationError("Profil utilisateur non trouvé.")
        
        return self.cleaned_data