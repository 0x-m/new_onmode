from rest_framework.routers import DefaultRouter
from .views import ShopAPIViewset

router = DefaultRouter()
router.register(r"shops", ShopAPIViewset, basename="shops")
