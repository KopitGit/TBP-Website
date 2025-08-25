# Fichier: accounts/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Entreprise, Profile

class AuthenticationTests(TestCase):
    def setUp(self):
        self.entreprise = Entreprise.objects.create(
            id_entreprise="TEST1234",
            nom="Test Entreprise",
            email="test@example.com",
            est_verifie=True
        )
    
    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Création de compte Admin')
    
    def test_entreprise_creation(self):
        self.assertEqual(self.entreprise.nom, "Test Entreprise")
        self.assertEqual(self.entreprise.id_entreprise, "TEST1234")
        self.assertTrue(self.entreprise.est_verifie)
    
    def test_profile_creation(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123"
        )
        
        profile = Profile.objects.get(user=user)
        profile.entreprise = self.entreprise
        profile.type_utilisateur = 'admin'
        profile.save()
        
        self.assertEqual(profile.entreprise, self.entreprise)
        self.assertEqual(profile.type_utilisateur, 'admin')