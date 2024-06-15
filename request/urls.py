from django.contrib import admin
from django.urls import path
from request.views import *

urlpatterns = [
    path('add-request/',add_request),
    path('get_list_request/<id_pemerintah_request>/',get_list_request),
    path('verify-request/<id>/',verify_request)
]