from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.hello, name="webcrud_hello"),

    path("building/<str:action>/", views.BuildingView.as_view(), name="building_action"),
    path("building/<str:action>/<int:id>/", views.BuildingView.as_view(), name="building_action_id"),

    path("street/<str:action>/", views.StreetView.as_view(), name="street_action"),
    path("street/<str:action>/<int:id>/", views.StreetView.as_view(), name="street_action_id"),

    path("poi/<str:action>/", views.PoiView.as_view(), name="poi_action"),
    path("poi/<str:action>/<int:id>/", views.PoiView.as_view(), name="poi_action_id"),
    path('webcrud/', include('webcrud.urls')),
]