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
]