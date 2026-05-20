#Your current webcrud/urls.py is wrong because it includes webcrud inside itself and uses views that do not exist yet.
from django.urls import path
from . import views

urlpatterns = [
    path("building/<str:action>/", views.BuildingView.as_view(), name="building_action"),
    path("building/<str:action>/<int:id>/", views.BuildingView.as_view(), name="building_action_id"),

    path("street/<str:action>/", views.StreetView.as_view(), name="street_action"),
    path("street/<str:action>/<int:id>/", views.StreetView.as_view(), name="street_action_id"),

    path("poi/<str:action>/", views.PoiView.as_view(), name="poi_action"),
    path("poi/<str:action>/<int:id>/", views.PoiView.as_view(), name="poi_action_id"),
]