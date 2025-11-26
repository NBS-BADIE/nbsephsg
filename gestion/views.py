from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .forms import ConnexionForm
from .models import CompteurVisites
from .models import Medecin, Service
from .forms import MedecinForm, ServiceForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import AppUser
from .forms import AppUserForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import update_session_auth_hash
from .models import Rapport
from django.core.mail import send_mail
from .models import MessageContact
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Service, UniteService, ServiceDetail, EffectifService, ActiviteService
from collections import defaultdict
from .forms import MedecinForm
from .models import Medecin
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os, json
from django.http import HttpResponse
from django.core.management import call_command
from django.http import HttpResponse
from django.core.management import call_command

# appliquer migration sur render
def apply_migrations(request):
    call_command('migrate')
    return HttpResponse("Migrations applied!")

# appliquer MAJ db data
def import_data(request):
    try:
        call_command('loaddata', 'data_clean.json')
        return HttpResponse("✅ Données importées avec succès dans la base PostgreSQL Render.")
    except Exception as e:
        return HttpResponse(f"❌ Erreur pendant l'import : {e}")



# =================== Migration ===================
def apply_migrations(request):
    call_command('migrate')
    return HttpResponse("Migrations applied!")

# =================== Compteur global ===================
def get_compteur(request):
    """
    Incrémente le compteur seulement si l'utilisateur n'a pas encore été compté
    dans cette session.
    """
    if not request.session.get('compteur_incremente', False):
        compteur, created = CompteurVisites.objects.get_or_create(id=1)
        if not created:
            compteur.nombre += 1
        else:
            compteur.nombre = 1
        compteur.save()
        request.session['compteur_incremente'] = True  # marque la session
    else:
        compteur = CompteurVisites.objects.first()
    return compteur.nombre if compteur else 0

# =================== Présentation de l'hopital ===================


def ephsg(request):
    specialites = [
        "Chirurgie",
        "Gynécologie & Obstétrique",
        "Anesthésie & Réanimation",
        "Pédiatrie & Néonatologie",
        "Radiologie & Biologie",
        "Rééducation & Médecine du travail"
    ]
    return render(request, "ephsg.html", {"specialites": specialites})






# =================== à propos ===================
def a_propos(request):
    return render(request, 'a_propos.html')

# =================== Accueil ===================
def accueil(request):
    date_heure = datetime.now()
    visiteur = request.session.get('visiteur', False)

    # Rôles
    is_admin = request.user.is_authenticated and getattr(request.user, 'role', '') == 'admin'
    is_moderateur = request.user.is_authenticated and getattr(request.user, 'role', '') == 'moderateur'
    is_utilisateur = request.user.is_authenticated and not (is_admin or is_moderateur)

    # Slides depuis JSON
    slides_file = os.path.join(settings.BASE_DIR, "static", "data", "slides.json")
    slides = []
    if os.path.exists(slides_file):
        with open(slides_file, "r", encoding="utf-8") as f:
            slides = json.load(f)

    # Vérifie que chaque slide a bien les clés attendues
    for slide in slides:
        slide.setdefault('image', '')
        slide.setdefault('title', '')
        slide.setdefault('slogan', '')

    return render(request, 'accueil.html', {
        'date_heure': date_heure,
        'visiteur': visiteur,
        'is_admin': is_admin,
        'is_moderateur': is_moderateur,
        'is_utilisateur': is_utilisateur,
        'user_role': getattr(request.user, 'role', None),
        'slides': slides,
    })

# =================== Accès visiteur ===================
def home(request):
    date_heure = datetime.now()
    visiteur = True
    request.session['visiteur'] = True
    #compteur_visites = get_compteur(request)

    return render(request, 'home.html', {
        'date_heure': date_heure,
        'visiteur': visiteur,
        #'compteur_visites': compteur_visites,
    })


# =================== Connexion ===================
def connexion(request):
    if request.user.is_authenticated:
        return redirect_dashboard(request.user)

    message = ''
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session.pop('visiteur', None)
            return redirect_dashboard(user)
        else:
            message = 'Nom d’utilisateur ou mot de passe incorrect.'
    else:
        form = ConnexionForm()

    #compteur_visites = get_compteur(request)
    return render(request, 'connexion.html', {
        'form': form,
        'message': message,
        'visiteur': request.session.get('visiteur', False),
       # 'compteur_visites': compteur_visites,
    })


# =================== Déconnexion ===================
def deconnexion(request):
    logout(request)
    request.session.pop('visiteur', None)
    return redirect('accueil')


# =================== Redirection selon rôle ===================
def redirect_dashboard(user):
    if hasattr(user, 'role'):
        if user.role == 'admin':
            return redirect('admin_dashboard')
        elif user.role == 'moderateur':
            return redirect('moderation')
        else:
            return redirect('home')
    return redirect('home')


# =================== ADMIN ===================
def admin_dashboard(request):
    User = get_user_model()

    # Comptes
    total_admins = User.objects.filter(role='admin').count()
    total_moderateurs = User.objects.filter(role='moderateur').count()
    total_utilisateurs = User.objects.filter(role='utilisateur').count()

    compteur_visites = 123  # exemple, à remplacer par ta logique réelle

    # Exemple de données graphiques
    labels_visites = ['Jan','Feb','Mar','Apr','May']
    data_visites = [50, 70, 80, 60, 90]

    services_labels = ['Cardio','Ortho','Pediatrie']
    services_data = [15, 10, 25]

    date_heure = datetime.now()

    # Liste cartes statistiques
    cartes_stats = [
        {'title': 'Visites totales', 'value': compteur_visites, 'icon': 'bi-people-fill', 'bg': 'rgba(0,153,255,0.3)'},
        {'title': 'Admins', 'value': total_admins, 'icon': 'bi-person-badge-fill', 'bg': 'rgba(0,123,255,0.3)'},
        {'title': 'Modérateurs', 'value': total_moderateurs, 'icon': 'bi-person-lines-fill', 'bg': 'rgba(255,193,7,0.3)'},
        {'title': 'Utilisateurs', 'value': total_utilisateurs, 'icon': 'bi-person-fill', 'bg': 'rgba(40,167,69,0.3)'},
    ]

    return render(request, 'admin_dashboard.html', {
        'total_admins': total_admins,
        'total_moderateurs': total_moderateurs,
        'total_utilisateurs': total_utilisateurs,
        'labels_visites': labels_visites,
        'data_visites': data_visites,
        'services_labels': services_labels,
        'services_data': services_data,
        'date_heure': date_heure,
        'user_role': getattr(request.user, 'role', None),
        'compteur_visites': compteur_visites,
        'cartes_stats': cartes_stats,  # ajouté pour le template
    })



def gestion_utilisateurs(request):
   # compteur_visites = get_compteur(request)
    return render(request, 'gestion_utilisateurs.html')


def rapports(request):
    #compteur_visites = get_compteur(request)
    return render(request, 'rapports.html')
    # (, {'compteur_visites': compteur_visites})

# =================== MODÉRATEUR ===================
def moderation(request):
    #compteur_visites = get_compteur(request)
    return render(request, 'moderation.html')

# ============================ Contacts ============================

def contacts(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message_txt = request.POST.get('message')

        # 1️⃣ Sauvegarde en BD
        MessageContact.objects.create(
            nom=nom,
            email=email,
            sujet=sujet,
            message=message_txt
        )

        # 2️⃣ Envoi e-mail
        send_mail(
            subject=f"Nouveau message : {sujet}",
            message=f"Nom : {nom}\nEmail : {email}\n\nMessage :\n{message_txt}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.CONTACT_RECIPIENTS,
            fail_silently=False,
        )

        messages.success(request, "Votre message a été envoyé avec succès.")
        return redirect('contact')

    return render(request, 'contacts.html')

# =================== LISTE DES UTILISATEURS ===================
def liste_utilisateurs(request):
    User = get_user_model()
    utilisateurs = User.objects.all()
    #compteur_visites = get_compteur(request)
    return render(request, 'liste_utilisateurs.html', {
        'utilisateurs': utilisateurs,
        #'compteur_visites': compteur_visites,
    })

# ================= MÉDECINS =================

# Liste des médecins
def liste_medecins(request):
    medecins = Medecin.objects.all().order_by('ordre')

    # Grades distincts
    grades = Medecin.objects.values_list("grade", flat=True).distinct().order_by("grade")

    # Fonctions distinctes
    fonctions = Medecin.objects.values_list("fonction", flat=True).distinct().order_by("fonction")

    # Spécialités distinctes
    specialites = Medecin.objects.values_list("specialite", flat=True).distinct().order_by("specialite")

    # Services distincts liés aux médecins
    services = Medecin.objects.values_list("service__nom", flat=True).distinct().order_by("service__nom")

    return render(request, "admin/medecins/liste.html", {
        "medecins": medecins,
        "grades": grades,
        "fonctions": fonctions,
        "specialites": specialites,
        "services": services,  # <-- ajouté pour le filtre
        'role': getattr(request.user, 'role', None)
    })



@csrf_exempt
def update_medecins_order(request):
    if request.method == "POST":
        ordre_list = request.POST.getlist("ordre[]")

        for index, medecin_id in enumerate(ordre_list):
            Medecin.objects.filter(id=medecin_id).update(ordre=index)

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error", "message": "Méthode non autorisée"})

# Ajouter un médecin
def ajouter_medecin(request):
    if request.method == "POST":
        form = MedecinForm(request.POST, request.FILES)  # Upload photo
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Médecin ajouté avec succès.")
            return redirect('liste_medecins')
        else:
            messages.error(request, "❌ Erreur : veuillez vérifier les champs du formulaire.")
    else:
        form = MedecinForm()

    return render(request, 'admin/medecins/medecin_form.html', {
        'form': form,
        'medecin': None
    })

# Modifier un médecin
def modifier_medecin(request, pk):
    medecin = get_object_or_404(Medecin, pk=pk)
    if request.method == "POST":
        form = MedecinForm(request.POST, request.FILES, instance=medecin)  # Upload photo
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Médecin modifié avec succès.")
            return redirect('liste_medecins')
        else:
            messages.error(request, "❌ Erreur : veuillez vérifier les champs du formulaire.")
    else:
        form = MedecinForm(instance=medecin)

    return render(request, "admin/medecins/medecin_form.html", {
        "form": form,
        "medecin": medecin
    })

# Supprimer un médecin
def supprimer_medecin(request, pk):
    medecin = get_object_or_404(Medecin, pk=pk)
    medecin.delete()
    messages.warning(request, "🗑️ Médecin supprimé avec succès !")
    return redirect('liste_medecins')


# ================= SERVICES =================

def liste_services(request):
    services = Service.objects.all().prefetch_related('unites').select_related('details', 'effectifs')

    # === CALCUL TOTAL EFFECTIFS ET LITS ===
    for s in services:
        if hasattr(s, 'effectifs') and s.effectifs:
            s.effectifs_total = (
                s.effectifs.professeurs +
                s.effectifs.specialistes +
                s.effectifs.generalistes +
                s.effectifs.paramedicaux +
                s.effectifs.autres
            )
        else:
            s.effectifs_total = 0

        if hasattr(s, 'details') and s.details:
            s.lits_total = s.details.nb_lits
        else:
            s.lits_total = 0

    context = {
        'services': services,
        'role': getattr(request.user, 'role', None),
    }
    return render(request, 'admin/services/liste_svc.html', context)


# Liste des services (guest)
def services_list(request):
    from gestion.models import Service
    services = Service.objects.all()
    return render(request, 'guest/services/services_list.html', {'services': services})

def ajouter_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ - Service ajouté avec succès ", extra_tags='service')
            return redirect('liste_services_svc')
    else:
        form = ServiceForm()
    return render(request, 'admin/services/ajouter_svc.html', {'form': form})

def modifier_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ - Service modifié avec succès !", extra_tags='service')
            return redirect('liste_services_svc')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'admin/services/modifier_svc.html', {'form': form, 'service': service})

def supprimer_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    messages.warning(request, "🗑️ - Service supprimé ", extra_tags='service')
    return redirect('liste_services_svc')



# ✔ Page principale : gérer un service
def service_manage(request, pk):
    service = get_object_or_404(Service, pk=pk)

    details = getattr(service, "details", None)
    effectifs = getattr(service, "effectifs", None)
    activite = getattr(service, "activite", None)
    unites = service.unites.all()

    return render(request, "admin/services/manage_service.html", {
        "service": service,
        "details": details,
        "effectifs": effectifs,
        "activite": activite,
        "unites": unites,
    })

# ✔ Modifier les détails
def service_details_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)

    details, created = ServiceDetail.objects.get_or_create(service=service)

    if request.method == "POST":
        details.nb_lits = request.POST.get("nb_lits")
        details.cout_journee = request.POST.get("cout_journee")
        details.save()

        messages.success(request, "Détails mis à jour.")
        return redirect("service_manage", pk=pk)

    return render(request, "admin/services/edit_details.html", {"service": service, "details": details})

# ✔ Modifier les effectifs
def service_effectifs_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    effectifs, created = EffectifService.objects.get_or_create(service=service)

    if request.method == "POST":
        effectifs.professeurs = request.POST["professeurs"]
        effectifs.specialistes = request.POST["specialistes"]
        effectifs.generalistes = request.POST["generalistes"]
        effectifs.paramedicaux = request.POST["paramedicaux"]
        effectifs.autres = request.POST["autres"]
        effectifs.save()

        messages.success(request, "Effectifs mis à jour.")
        return redirect("service_manage", pk=pk)

    return render(request, "admin/services/edit_effectifs.html", {
        "service": service,
        "effectifs": effectifs,
    })


# ✔ Modifier activité
def service_activite_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    activite, created = ActiviteService.objects.get_or_create(service=service)

    if request.method == "POST":
        activite.admissions = request.POST["admissions"]
        activite.journees_hospitalisation = request.POST["journees_hospitalisation"]
        activite.taux_occupation = request.POST["taux_occupation"]
        activite.duree_moy_sejour = request.POST["duree_moy_sejour"]
        activite.taux_mortalite = request.POST["taux_mortalite"]
        activite.save()

        messages.success(request, "Activité mise à jour.")
        return redirect("service_manage", pk=pk)

    return render(request, "admin/services/edit_activite.html", {
        "service": service,
        "activite": activite,
    })

# ✔ CRUD des unités


def unites_list(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    unites = UniteService.objects.filter(service=service)

    return render(request, 'admin/services/unites/unites_list.html', {
        'service': service,
        'unites': unites
    })

def unite_add(request, service_id):
    service = get_object_or_404(Service, pk=service_id)

    if request.method == "POST":
        nom = request.POST.get("nom")
        description = request.POST.get("description")
        lits = request.POST.get("lits") or 0  # récupère le nombre de lits

        UniteService.objects.create(
            service=service,
            nom=nom,
            description=description,
            lits=int(lits)
        )

        messages.success(request, "Unité ajoutée avec succès.")
        return redirect('unites_list', service_id=service.id)

    return render(request, 'admin/services/unites/unite_add.html', {
        'service': service
    })


def unite_edit(request, unite_id):
    unite = get_object_or_404(UniteService, pk=unite_id)
    service = unite.service

    if request.method == "POST":
        unite.nom = request.POST.get("nom")
        unite.description = request.POST.get("description")
        unite.lits = int(request.POST.get("lits") or 0)
        unite.save()
        messages.success(request, "Unité mise à jour avec succès.")
        return redirect('unites_list', service_id=service.id)

    return render(request, 'admin/services/unites/unite_edit.html', {
        'unite': unite,
        'service': service
    })


def unite_delete(request, pk):
    
    unite = get_object_or_404(UniteService, pk=pk)
    service_id = unite.service.id
    unite.delete()
    messages.success(request, "Unité supprimée avec succès.")
    return redirect('service_manage', pk=service_id)

# Liste des utilisateurs
def liste_usr(request):
    utilisateurs = AppUser.objects.all()
    return render(request, 'admin/utilisateurs/liste_usr.html', {'utilisateurs': utilisateurs})



# Ajouter un utilisateur
def ajouter_usr(request):
    if request.method == "POST":
        form = AppUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)  # hash du mot de passe
            user.save()
            return redirect('liste_usr')
    else:
        form = AppUserForm()
    return render(request, 'admin/utilisateurs/utilisateurs_form.html', {'form': form, 'titre': 'Ajouter un utilisateur'})

# Modifier un utilisateur
def modifier_usr(request, pk):
    user = get_object_or_404(AppUser, pk=pk)
    if request.method == "POST":
        form = AppUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)  # garde la session active si connecté
            else:
                user.save()
            return redirect('liste_usr')
    else:
        form = AppUserForm(instance=user)
    return render(request, 'admin/utilisateurs/utilisateurs_form.html', {'form': form, 'titre': 'Modifier un utilisateur'})

   

# Supprimer utilisateur
def supprimer_usr(request, pk):
    utilisateur = get_object_or_404(AppUser, pk=pk)
    utilisateur.delete()
    messages.warning(request, "Utilisateur supprimé 🗑️", extra_tags='utilisateur')
    return redirect('liste_usr')

# Envois mail
def test_email(request):
    send_mail(
        'Test Django',
        'Ça fonctionne !',
        'ephsg1985@gmail.com',
        ['ephsg1985@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("Email envoyé !")

# =============================Services mode Invité =========================
def services_list_guest(request):
    services = Service.objects.all().order_by('nom')
    return render(request, 'guest/services/services_list.html', {
        'services': services
    })


def service_detail_guest(request, pk):
    service = get_object_or_404(Service, pk=pk)

    # Récupérer tous les médecins du service
    medecins = service.medecins.all()
    # Regrouper les médecins par grade en nettoyant les espaces
    medecins_par_grade = defaultdict(list)
    for m in medecins:
        grade = m.grade.strip() if m.grade else "Non défini"
        medecins_par_grade[grade].append(m)

    # Trier les grades dans l'ordre décroissant
    ordre_grades = ["Professeur", "Spécialiste", "Médecin généraliste"]
    ordre_grades.reverse()  # Pour décroissant : Professeur → Spécialiste → Médecin généraliste

    medecins_par_grade_trie = {}
    for grade in ordre_grades:
        if grade in medecins_par_grade:
            medecins_par_grade_trie[grade] = medecins_par_grade[grade]

    # Ajouter les autres grades non prévus à la fin
    for grade, med_list in medecins_par_grade.items():
        if grade not in medecins_par_grade_trie:
            medecins_par_grade_trie[grade] = med_list

    # Infos complémentaires du service
    details = getattr(service, "details", None)
    effectifs = getattr(service, "effectifs", None)
    activite = getattr(service, "activite", None)
    unites = service.unites.all()
    total_lits = sum(u.lits for u in unites)

    return render(request, "guest/services/service_detail.html", {
        "service": service,
        "details": details,
        "effectifs": effectifs,
        "activite": activite,
        "unites": unites,
        "total_lits": total_lits,
        "medecins_par_grade": medecins_par_grade_trie,
    })
