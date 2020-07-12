from django.urls import path
from lore_app import views

app_name = "lore_app"

urlpatterns = [
    path("", views.attacks_view, name="attacks_view"),
    path("data/", views.attack_protocol_data, name="attack_protocol_data"),
    path("host/", views.attack_host_data, name="attack_host_data"),
    path("hostproto/", views.attack_protocol_host_data, name="attack_protocol_host_data"),

]
