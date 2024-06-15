from django.contrib import admin
from django.urls import path
from negosiasi_request.views import *

urlpatterns = [
    path('add-negosiasi-request/',add_negosiasi_request),
    path('get-negosiasi-request/',get_list_negosiasi_request)
]