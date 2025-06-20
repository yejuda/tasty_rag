from django.urls import path, include
from rest_framework.routers import DefaultRouter # DefaultRouter로 ViewSet 자동 라우팅
from .views import RestaurantViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]