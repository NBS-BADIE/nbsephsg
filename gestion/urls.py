from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    
    # ================= ACCUEIL / VISITEUR =================
    path('apply-migrations/', views.apply_migrations, name='apply_migrations'),
    path('import-data/', views.import_data, name='import_data'),
    path('list-static/', views.list_static),


    # ================= ACCUEIL / VISITEUR =================
    path('', views.accueil, name='accueil'),
    path('home/', views.home, name='home'),  # page visiteur après clic
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('redirect/', views.redirect_dashboard, name='redirect_dashboard'),
    path("ephsg/", views.ephsg, name="ephsg"),
<<<<<<< Updated upstream
    path('a-propos/', views.a_propos, name='a_propos'),
=======
>>>>>>> Stashed changes


    # ================= ADMIN PERSONNALISÉ =================
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('dashboard/rapports/', views.rapports, name='rapports'),
    path('liste_utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    # ================= UNITES (ADMIN) =================
    path('dashboard/services/<int:service_id>/unites/', views.unites_list, name='unites_list'),
    path('dashboard/services/<int:service_id>/unites/ajouter/', views.unite_add, name='unite_add'),
    path('dashboard/unites/<int:pk>/modifier/', views.unite_edit, name='unite_edit'),
    path('dashboard/services/unites/<int:pk>/supprimer/', views.unite_delete, name='unite_delete'),

    # ================= MODÉRATEUR =================
    path('moderation/', views.moderation, name='moderation'),

    # ================= MÉDECINS =================
    path('dashboard/medecins/', views.liste_medecins, name='liste_medecins'),
    path('dashboard/medecins/ajouter/', views.ajouter_medecin, name='ajouter_medecin'),
    path('dashboard/medecins/modifier/<int:pk>/', views.modifier_medecin, name='modifier_medecin'),
    path('dashboard/medecins/supprimer/<int:pk>/', views.supprimer_medecin, name='supprimer_medecin'),
    path("medecins/update-order/",views.update_medecins_order,name="update_medecins_order"),

   
    # ================= SERVICES =================
    path('dashboard/services/', views.liste_services, name='liste_services_svc'),
    path('dashboard/services/ajouter/', views.ajouter_service, name='ajouter_service_svc'),
    path('dashboard/services/modifier/<int:pk>/', views.modifier_service, name='modifier_service_svc'),
    path('dashboard/services/supprimer/<int:pk>/', views.supprimer_service, name='supprimer_service_svc'),
    # -------- GESTION AVANCÉE DES SERVICES --------
    path('dashboard/services/<int:pk>/gerer/', views.service_manage, name='service_manage'),
    # Détails du service
    path('dashboard/services/<int:pk>/details/', views.service_details_edit, name='service_details_edit'),
    # Effectifs
    path('dashboard/services/<int:pk>/effectifs/', views.service_effectifs_edit, name='service_effectifs_edit'),
    # Activité
    path('dashboard/services/<int:pk>/activite/', views.service_activite_edit, name='service_activite_edit'),
    # Unités du service
    path('dashboard/services/<int:pk>/unites/', views.unites_list, name='unites_list'),
    path('dashboard/services/<int:pk>/unites/ajouter/', views.unite_add, name='unite_add'),
    path('dashboard/services/unites/<int:unite_id>/modifier/', views.unite_edit, name='unite_edit'),
    path('dashboard/services/unites/<int:unite_id>/supprimer/', views.unite_delete, name='unite_delete'),





    # ================= GUEST : SERVICES =================
    path('services/', views.services_list_guest, name='services_list'),
    path('services/<int:pk>/', views.service_detail_guest, name='service_detail'),
    path('guest/services/<int:pk>/', views.service_detail_guest, name='service_detail_guest'),


    
    
    # ================= Utilistateurs =================
    path('dashboard/utilisateurs/liste/', views.liste_usr, name='liste_usr'),
    path('dashboard/utilisateurs/ajouter/', views.ajouter_usr, name='ajouter_usr'),
    path('dashboard/utilisateurs/modifier/<int:pk>/', views.modifier_usr, name='modifier_usr'),
    path('dashboard/utilisateurs/supprimer/<int:pk>/', views.supprimer_usr, name='supprimer_usr'),

    # ========================= Contacts =================
    path('contact/', views.contacts, name='contact'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
