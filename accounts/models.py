

# Fichier: accounts/models.py
import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Entreprise(models.Model):
    id_entreprise = models.CharField(max_length=8, unique=True, primary_key=True)
    nom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    est_verifie = models.BooleanField(default=False)
    
    def generer_id_entreprise(self):
        return ''.join(random.choices(string.ascii_uppercase, k=8))
    
    def save(self, *args, **kwargs):
        if not self.id_entreprise:
            self.id_entreprise = self.generer_id_entreprise()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nom

class Profile(models.Model):
    TYPES_UTILISATEUR = (
        ('admin', 'Administrateur'),
        ('co-admin', 'Co-Administrateur'),
        ('manageur', 'Manageur'),
        ('tierce', 'Tierce'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    type_utilisateur = models.CharField(max_length=20, choices=TYPES_UTILISATEUR)
    telephone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    droits_creation_utilisateur = models.BooleanField(default=False)
    droits_edition_profile = models.BooleanField(default=False)
    droits_voir_caisse = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.entreprise.nom}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
