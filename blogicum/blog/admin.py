from django.contrib import admin

from .models import Category, Location, Post, Comment

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Location)
admin.site.register(Post)
