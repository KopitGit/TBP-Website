# Fichier: accounts/views.py
import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Entreprise, Profile
from .forms import RegisterForm, OTPVerificationForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Générer OTP
            otp = str(random.randint(100000, 999999))
            
            # Créer l'entreprise sans la sauvegarder encore
            entreprise = Entreprise(
                nom=form.cleaned_data['nom_entreprise'],
                email=form.cleaned_data['email']
            )
            
            # Stocker les données en session pour plus tard
            request.session['register_data'] = {
                'nom_entreprise': form.cleaned_data['nom_entreprise'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password1'],
                'otp': otp,
                'entreprise_id': entreprise.generer_id_entreprise()
            }
            
            # Envoyer l'email avec l'OTP
            send_mail(
                'Vérification de votre compte Tbp-Website',
                f'Votre code OTP est: {otp}. Votre ID entreprise est: {request.session["register_data"]["entreprise_id"]}',
                settings.DEFAULT_FROM_EMAIL,
                [form.cleaned_data['email']],
                fail_silently=False,
            )
            
            messages.success(request, 'Un code OTP a été envoyé à votre adresse email.')
            return redirect('verification_otp')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def verification_otp(request):
    if 'register_data' not in request.session:
        return redirect('register')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_saisi = form.cleaned_data['otp']
            otp_session = request.session['register_data']['otp']
            
            if otp_saisi == otp_session:
                # Créer l'entreprise
                entreprise = Entreprise.objects.create(
                    id_entreprise=request.session['register_data']['entreprise_id'],
                    nom=request.session['register_data']['nom_entreprise'],
                    email=request.session['register_data']['email'],
                    est_verifie=True
                )
                
                # Créer l'utilisateur admin
                user = User.objects.create_user(
                    username=request.session['register_data']['email'],
                    email=request.session['register_data']['email'],
                    password=request.session['register_data']['password']
                )
                
                # Créer le profil admin
                profile = Profile.objects.get(user=user)
                profile.entreprise = entreprise
                profile.type_utilisateur = 'admin'
                profile.droits_creation_utilisateur = True
                profile.droits_edition_profile = True
                profile.droits_voir_caisse = True
                profile.save()
                
                # Connecter l'utilisateur
                login(request, user)
                
                # Nettoyer la session
                del request.session['register_data']
                
                messages.success(request, 'Votre compte a été créé avec succès!')
                return redirect('accueil')
            else:
                messages.error(request, 'Code OTP incorrect.')
    else:
        form = OTPVerificationForm()
    
    return render(request, 'accounts/verification_otp.html', {'form': form})