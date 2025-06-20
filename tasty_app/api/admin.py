# Restaurant/Review를 관리자에서 관리

from django.contrib import admin
from .models import Restaurant, Review

admin.site.register(Restaurant)
admin.site.register(Review)