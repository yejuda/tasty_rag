# Django 모델 인스턴스(python객체나 쿼리셋)를 JSON 형태로 변환 (복잡한 객체 -> 간단한 JSON)

from rest_framework import serializers
from .models import Restaurant, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'