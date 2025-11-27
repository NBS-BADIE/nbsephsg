from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

# === Définition des rôles ===
ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('moderateur', 'Modérateur'),
    ('utilisateur', 'Utilisateur'),
]

# === Compteur de visites ===
class CompteurVisites(models.Model):
    nombre = models.IntegerField(default=0)

    def __str__(self):
        return str(self.nombre)


# ============================================================================================
# === SERVICE DOIT ETRE DÉCLARÉ AVANT MEDECIN (IMPORTANT !)
# ============================================================================================

class Service(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)  # ✅ Cloudinary

    def __str__(self):
        return self.nom


class ServiceDetail(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE, related_name="details")
    nb_lits = models.PositiveIntegerField(default=0)
    cout_journee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Détails : {self.service.nom}"


class EffectifService(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE, related_name="effectifs")
    professeurs = models.PositiveIntegerField(default=0)
    specialistes = models.PositiveIntegerField(default=0)
    generalistes = models.PositiveIntegerField(default=0)
    paramedicaux = models.PositiveIntegerField(default=0)
    autres = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Effectifs {self.service.nom}"


# === Unités du service ===
class UniteService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="unites")
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    lits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nom} ({self.service.nom})"


# === Activité ===
class ActiviteService(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE, related_name="activite")
    admissions = models.PositiveIntegerField(default=0)
    journees_hospitalisation = models.PositiveIntegerField(default=0)
    taux_occupation = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    duree_moy_sejour = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    taux_mortalite = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"Activité {self.service.nom}"


# ============================================================================================
# === MEDECIN
# ============================================================================================

GRADE_CHOICES = [
    ('Généraliste', 'Généraliste'),
    ('Généraliste Chef', 'Généraliste Chef'),
    ('Résident', 'Résident'),
    ('Praticien Spécialiste Assistant', 'Praticien Spécialiste Assistant'),
    ('Praticien Spécialiste Chef', 'Praticien Spécialiste Chef'),
    ('Praticien Spécialiste Principal', 'Praticien Spécialiste Principal'),
    ('Professeur', 'Professeur'),
]

FONCTION_CHOICES = [
    ('Chef de Service', 'Chef de Service'),
    ('Chef d Unité', 'Chef d Unité'),
    ('Coordinateur', 'Coordinateur'),
    ('Médecin', 'Médecin'),
]

class Medecin(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="medecins")
    unite = models.ForeignKey(UniteService, on_delete=models.SET_NULL, related_name="medecins", null=True, blank=True)
    nom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    grade = models.CharField(max_length=50, choices=GRADE_CHOICES, default='Généraliste')
    fonction = models.CharField(max_length=50, choices=FONCTION_CHOICES, blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    photo = CloudinaryField('photo', blank=True, null=True)  # ✅ Cloudinary
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return f"{self.nom} - {self.specialite}"


# ============================================================================================
# === UTILISATEUR
# ============================================================================================

class AppUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('moderateur', 'Modérateur'),
        ('visiteur', 'Visiteur'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='visiteur')

    groups = models.ManyToManyField(
        Group,
        related_name="appuser_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="appuser_permissions_set",
        blank=True,
    )

    def __str__(self):
        return self.username


# ============================================================================================
# === RAPPORT & CONTACT
# ============================================================================================

class Rapport(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre


class MessageContact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=150)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.sujet}"
