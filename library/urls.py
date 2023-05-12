from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from library import views

router = routers.DefaultRouter()
router.register('papers', views.PaperViewSet)
router.register('authors', views.AuthorViewSet)
router.register('keywords', views.KeywordViewSet)
router.register('pdfs', views.PDFViewSet)
router.register('notes', views.NoteViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/bibtex/', views.bibtex),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token),
    path('django-rq/', include('django_rq.urls'))

]

