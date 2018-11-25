from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='listenings'),
    path('<int:listing_id>', views.listening, name='listening'),
    path('search', views.search, name='search'),
]