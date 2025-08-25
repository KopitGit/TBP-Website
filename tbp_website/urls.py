# Fichier: tbp_website/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.accueil, name='accueil'),
    path('register/', account_views.register, name='register'),
    path('verification-otp/', account_views.verification_otp, name='verification_otp'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=account_views.CustomAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dossier/', include('dossier.urls')),
    path('tiers/', include('tiers.urls')),
    path('facturation/', include('facturation.urls')),
    path('caisse/', include('caisse.urls')),
    path('analytics/', include('analytics.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)