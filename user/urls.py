from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("login/", CustomObtainAuthToken.as_view()),
    path("update-user-role/<str:user_id>/", update_user_role),
    path("logout/", logout),
    path("get-token-by-user/<str:token_key>/", get_token_by_user),
    path("get-list-user/", get_list_user),
    path("logged-in/",get_user_view),
    path("add-user/",add_user),
    path('get-petani-daerah/<daerah>/',get_list_petani_daerah)
]
