from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path("delete_account/<str:username>", views.delete_account, name="delete_account"),
    path("emergency_contact/", views.emergency_contact, name="emergency_contact"),
    path("create_contact/", views.createContact, name="create_contact"),
    path("update_contact/<str:pk>/", views.update_contact, name="update_contact"),
    path("delete_contact/<str:pk>/", views.delete_contact, name="delete_contact"),
    path("emergency/", views.emergency, name="emergency"),
    path('women_rights/', views.women_rights, name='women_rights'),
    path("women_laws/", views.women_laws, name="women_laws"),
    path("helpline_numbers/", views.helpline_numbers, name="helpline_numbers"),
    path('ngo_details/', views.ngo_details, name='ngo_details'),
    path('gallery/', views.gallery, name='gallery'),
]