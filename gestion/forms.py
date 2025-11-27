from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import AppUser, UniteService, Medecin, Service
from cloudinary.models import CloudinaryField

# ========================= Connexion =========================
class ConnexionForm(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Entrez votre nom d'utilisateur"
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Entrez votre mot de passe"
        })
    )


# ========================= Service =========================
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['nom', 'description', 'image']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# ========================= Médecin =========================
class MedecinForm(forms.ModelForm):
    class Meta:
        model = Medecin
        fields = [
            'nom', 'specialite', 'telephone', 'email',
            'service', 'unite', 'grade', 'fonction', 'photo'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'specialite': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'unite': forms.Select(attrs={'class': 'form-select'}),
            'grade': forms.Select(attrs={'class': 'form-select'}),
            'fonction': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# ========================= AppUser =========================
class AppUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
        required=False,  # optionnel pour modification
        label="Mot de passe"
    )

    class Meta:
        model = AppUser
        fields = ['username', 'email', 'role', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg'}),
            'role': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_active': 'Actif',
        }


# ========================= UniteService =========================
class UniteServiceForm(forms.ModelForm):
    class Meta:
        model = UniteService
        fields = ['nom', 'description', 'lits']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'lits': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
