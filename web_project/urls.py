from django.contrib import admin
from django.urls import path
from ai_models import views

urlpatterns = [
    # 1. Admin Portal
    path('admin/', admin.site.urls),
    
    # 2. Home Page Route
    path('', views.home_view, name='home'),
    
    # 3. Dedicated Page Routes (Nav-bar links)
    path('languages/', views.languages_page, name='languages_page'),
    path('models/', views.models_page, name='models_page'),
    path('leaderboard/', views.leaderboard_page, name='leaderboard_page'),
    path('compare/', views.compare_page, name='compare_page'),
    path('api-keys/', views.api_keys_page, name='api_keys_page'),
    path('publications/', views.publications_page, name='publications_page'),
    path('publications/<slug:slug>/', views.publication_detail, name='publication_detail'),
    
    # 4. Individual Model Detail Sub-routes
    path('models/asr/', views.model_detail_asr, name='model_asr'),
    path('models/lid/', views.model_detail_lid, name='model_lid'),
    path('models/dialect/', views.model_detail_dialect, name='model_dialect'),

    # 5. SYSPIN Dataset Hub & Complete Sub-routes
    path('dataset/syspin/', views.syspin_view, name='dataset_syspin'),
    path('dataset/syspin/languages/', views.syspin_languages_view, name='dataset_syspin_languages'),
    path('dataset/syspin/models/', views.syspin_models_view, name='dataset_syspin_models'),
    path('dataset/syspin/leaderboard/', views.syspin_leaderboard_view, name='dataset_syspin_leaderboard'),
    path('dataset/syspin/api-keys/', views.syspin_apikeys_view, name='dataset_syspin_apikeys'),
    path('dataset/syspin/publications/', views.syspin_publications_view, name='dataset_syspin_pubs'),

    # 6. RESPIN Dataset Hub & Complete Sub-routes
    path('dataset/respin/', views.respin_view, name='dataset_respin'),
    path('dataset/respin/languages/', views.respin_languages_view, name='dataset_respin_languages'),
    path('dataset/respin/models/', views.respin_models_view, name='dataset_respin_models'),
    path('dataset/respin/leaderboard/', views.respin_leaderboard_view, name='dataset_respin_leaderboard'),
    path('dataset/respin/api-keys/', views.respin_apikeys_view, name='dataset_respin_apikeys'),
    path('dataset/respin/publications/', views.respin_pubs_view, name='dataset_respin_pubs'),
    
    # 7. SPICOR Dataset Hub & Complete Sub-routes
    path('dataset/spicor/', views.spicor_view, name='dataset_spicor'),
    path('dataset/spicor/languages/', views.spicor_languages_view, name='dataset_spicor_languages'),
    path('dataset/spicor/models/', views.spicor_models_view, name='dataset_spicor_models'),
    path('dataset/spicor/leaderboard/', views.spicor_leaderboard_view, name='dataset_spicor_leaderboard'),
    path('dataset/spicor/apikeys/', views.spicor_apikeys_view, name='dataset_spicor_apikeys'),
    path('dataset/spicor/publications/', views.spicor_pubs_view, name='dataset_spicor_pubs'),
    
      # 8. VAANI Dataset Hub & Complete Sub-routes
    path('dataset/vaani/', views.vaani_view, name='dataset_vaani'),
    path('dataset/vaani/languages/', views.vaani_languages_view, name='dataset_vaani_languages'),
    path('dataset/vaani/models/', views.vaani_models_view, name='dataset_vaani_models'),
    path('dataset/vaani/leaderboard/', views.vaani_leaderboard_view, name='dataset_vaani_leaderboard'),
    path('dataset/vaani/apikeys/', views.vaani_apikeys_view, name='dataset_vaani_apikeys'),
    path('dataset/vaani/publications/', views.vaani_pubs_view, name='dataset_vaani_pubs'),
]
