from django.urls import path
from . import views

urlpatterns = [
    path("data/", views.api_data),
    path("recibir/", views.recibir_dato),
]
