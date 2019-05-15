from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CarModelViewSet, CarModelModelViewSet, ProducerModelViewSet
router = DefaultRouter()
router.register('cars', CarModelViewSet)
router.register('carmodels', CarModelModelViewSet)
router.register('producers', ProducerModelViewSet)

urlpatterns = [
    path('', include(router.urls))

]