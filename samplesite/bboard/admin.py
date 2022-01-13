from django.contrib import admin
from .models import Bd, Rubric


# class editor for admin representation
class BdAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    list_display_links = ('title', 'content', 'rubric')
    search_fields = ('title', 'content')


# Register your models here.
admin.site.register(Bd, BdAdmin)
admin.site.register(Rubric)
