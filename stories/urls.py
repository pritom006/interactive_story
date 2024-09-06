from django.urls import path
from . import views

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('<int:pk>/', views.story_detail, name='story_detail'),
    path('node/<int:node_id>/', views.node_detail, name='node_detail'),
    path('create/', views.create_story, name='create_story'),
    path('<int:story_pk>/create_node/', views.create_story_node, name='create_story_node'),
    path('node/<int:node_id>/create_choice/', views.create_story_choice, name='create_story_choice'),
    path('choice/<int:choice_id>/edit/', views.edit_story_choice, name='edit_story_choice'),
    path('<int:pk>/analytics/', views.story_analytics, name='story_analytics'),
]
