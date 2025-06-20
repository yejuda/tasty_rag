# CRUD가 가능한 RESTful API 자동 생성

from rest_framework import viewsets
from .models import Restaurant, Review
from .serializers import RestaurantSerializer, ReviewSerializer

class RestaurantViewSet(viewsets.ModelViewSet):  # ModelViewSet을 사용해 CRUD 자동 지원
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer