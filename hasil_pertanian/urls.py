from django.contrib import admin
from django.urls import path
from hasil_pertanian.views import *

urlpatterns = [
    path('add-hasil-pertanian/',add_hasil_pertanian),
    path('update-hasil-pertanian/',update_hasil_pertanian),
    path('get-hasil-pertanian/',get_list_hasil_pertanian),
    path('get-list-pertanian-daerah/<daerah>/<jenis_tanaman>/',get_list_hasil_pertanian_daerah)
]