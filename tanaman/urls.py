from django.contrib import admin
from django.urls import path
from tanaman.views import *

urlpatterns = [
    path('get-list-tanaman/<daerah>/',get_list_tanaman_daerah),
    path('add-tanaman/',add_tanaman)
]