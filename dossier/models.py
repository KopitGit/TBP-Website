# Fichier: dossier/models.py
from django.db import models
from accounts.models import Entreprise

class Dossier(models.Model):
    ETATS = (
        ('cloture', 'Clôturé'),
        ('encours', 'En Cours'),
        ('bloque', 'Bloqué'),
    )
    
    id_dossier = models.AutoField(primary_key=True)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    manif = models.CharField(max_length=255)
    client = models.ForeignKey('tiers.Client', on_delete=models.CASCADE)
    cies = models.CharField(max_length=255)
    n_bl = models.CharField(max_length=255, verbose_name="N° BL")
    n_tc = models.CharField(max_length=255, verbose_name="N° TC")
    dpi = models.DateField(verbose_name="Date de prise en charge")
    transporteur = models.CharField(max_length=255)
    p_tspt = models.CharField(max_length=255, verbose_name="Pays du transporteur")
    badval = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valeur déclarée")
    etat_livraison = models.CharField(max_length=255)
    tdst = models.CharField(max_length=255, verbose_name="Type de transport")
    etat = models.CharField(max_length=20, choices=ETATS, default='encours')
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id_dossier} - {self.manif}"

class Prestation(models.Model):
    ETATS_PAIEMENT = (
        ('paye', 'Payé'),
        ('partiel', 'Partiellement payé'),
        ('impaye', 'Impayé'),
    )
    
    MOYENS_PAIEMENT = (
        ('cash', 'Cash'),
        ('compte_client', 'Compte Client'),
        ('virement', 'Virement'),
        ('cheque', 'Chèque'),
    )
    
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='prestations')
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cout_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.IntegerField()
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    etat_paiement = models.CharField(max_length=20, choices=ETATS_PAIEMENT, default='impaye')
    moyen_paiement = models.CharField(max_length=20, choices=MOYENS_PAIEMENT, blank=True)
    date_paiement = models.DateField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.montant_total = self.cout_unitaire * self.quantite
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nom} - {self.dossier.id_dossier}"

class DocumentPrestation(models.Model):
    prestation = models.ForeignKey(Prestation, on_delete=models.CASCADE, related_name='documents')
    fichier = models.FileField(upload_to='documents/prestations/')
    nom = models.CharField(max_length=255)
    date_upload = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nom} - {self.prestation.nom}"