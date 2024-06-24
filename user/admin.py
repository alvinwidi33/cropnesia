from django.contrib import admin
from user.models import User,Pemerintah,Petani,Admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username','name','email','role','daerah')
    list_display = ("user_id",'username','name','email','role','daerah','datetime_created')

@admin.register(Pemerintah)
class PemerintahAdmin(admin.ModelAdmin):
    fields = ("user",)
    list_display= ("user_id","user")

@admin.register(Petani)
class PetaniAdmin(admin.ModelAdmin):
    fields = ("user",)
    list_display= ("user_id","user")

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    fields = ("user",)
    list_display= ("user_id","user")