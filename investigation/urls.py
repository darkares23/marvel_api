# investigation/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('populate/', views.populate, name='populate'),
    path('characters/', views.all_characters, name='all_characters'),
    path('characters/<int:character_id>/', views.character_detail, name='character_detail'),
    path('characters/delete/', views.delete_character_by_name, name='delete_character_by_name'),
    path('export_csv/', views.export_characters_csv, name='export_characters_csv'),
]
