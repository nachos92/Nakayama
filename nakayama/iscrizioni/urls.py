from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('iscritto/<int:iscritto_id>/', views.dettaglio_iscritto, name='detail'),

]
