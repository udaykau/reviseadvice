from django.contrib import admin
from .models import Registration, Movies, contact
# Register your models here.


class registration(admin.ModelAdmin):
    list_display = ('sno', 'username', 'email', 'date')


class movies(admin.ModelAdmin):
    list_display = ('sno', 'name', 'rating', 'releasing_date', 'date')


class Contact(admin.ModelAdmin):
    list_display = ('sno', 'name', 'phone_number', 'email', 'date')


admin.site.register(Registration, registration)
admin.site.register(Movies, movies)
admin.site.register(contact, Contact)