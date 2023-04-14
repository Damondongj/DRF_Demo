from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"articles", viewset=views.ArticleViewSet)

urlpatterns = []

urlpatterns += router.urls


