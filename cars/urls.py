from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CarModelViewset, CarModelModelViewset, ProducerModelViewset
router = DefaultRouter()
router.register('cars', CarModelViewset)
router.register('carmodels', CarModelModelViewset)
router.register('producers', ProducerModelViewset)

urlpatterns = [
    path('', include(router.urls))

]