from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_recipient", views.new_recipient, name="new_recipient_form_page"),
    path("add_recipient", views.add_recipient, name="add_recipient"),
    path("get_recipients", views.get_recipients, name="get_recipients"),
    path("vaccines_page/<int:rec_id>", views.vaccines_page, name="vaccines_page"),
    path("get_vaccines/<int:rec_id>", views.get_vaccines, name="get_vaccines"),
    path("toggle_vaccine_status", views.toggle_vaccine_status,
         name="toggle_vaccine_status"),
    path("log_out", views.user_logout, name="log_out"),
    path("delete_recipient/<int:rec_id>",
         views.delete_recipient, name="delete_recipient")
]

#from VacciSafeApp import execute