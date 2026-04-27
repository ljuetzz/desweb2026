from django.urls import path, include
from . import views
from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register(r'buildings', views.BuildingsModelViewSet)
#router.register(r'owners', views.OwnersModelViewSet)
#router.register(r'buildingsowners', views.BuildingsOwnersModelViewSet)
#

urlpatterns = [
    path("hello_world/", views.HelloWorldValenciaEramsus.as_view()),
    #path('', include(router.urls)),
    #path('buildings_view/<str:action>/', views.BuildigsView.as_view(), name='buildings_views'),  # POST requests
    #path('buildings_view/<str:action>/<int:id>/', views.BuildigsView.as_view(), name='buildings_views'),  # POST requests
    path("buildings/", views.BuildingView.as_view()),
    path("buildings/<str:action>/", views.BuildingView.as_view(), name='buildings_views'),  # POST requests
    path("buildings/<str:action>/<int:id>/", views.BuildingView.as_view(), name='buildings_views'),  # POST requests

    path("streets/", views.StreetView.as_view()),
    path("streets/<str:action>/", views.StreetView.as_view(), name='streets_views'),  # POST requests
    path("streets/<str:action>/<int:id>/", views.StreetView.as_view(), name='streets_views'),  # POST requests

    path("pois/", views.POIView.as_view()),
    path("pois/<str:action>/", views.POIView.as_view(), name='pois_views'),  # POST requests
    path("pois/<str:action>/<int:id>/", views.POIView.as_view(), name='pois_views'),  # POST requests
]