import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

#from djangoapi.codelist import models
from . import models

# import our own django models, which are the interface to the database
from scripts.p1.streetsDjangoModels.street import Street
from scripts.p1.buildingsDjangoModels.building import Building
from scripts.p1.poiDjangoModels.poi import POI

from django.contrib.gis.geos import GEOSGeometry

# Create your views here.

class HelloWorldValenciaEramsus(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Erasmus Valencia. Hello world", "data":[]},status=200)
    def post(self, request):
        data={}
        #data['id'] = request.POST.get('id', None)
        data['area'] = request.POST.get('area', None)
        data['height'] = request.POST.get('height', None)
        data['width'] = request.POST.get('width', None)
        return JsonResponse({"ok":True,"message": "Erasmus Valencia. Hello world", "data": [data]}, status=200)

class BuildingView(View):

    def get(self, request, **kwargs):

        building = Building()

        action = kwargs.get('action', None)
        if action == 'selectone':
            id = kwargs.get('id', None)
            return JsonResponse(building.selectOne(id), status=200)
        elif action == 'selectall':
            return JsonResponse(building.selectAll(), status=200)
        else:
            return JsonResponse({"ok":False,"message": "Invalid action, only 'selectone' and 'selectall' are allowed with GET requests!", "data":[]},status=200)
    
    def post(self, request, **kwargs):

        action = kwargs.get('action', None)
        building = Building()

        data = {}
        data['id'] = request.POST.get('id', None)
        print(f"data id: {data['id']}")
        data['height'] = request.POST.get('height', None)
        data['geom'] = request.POST.get('geom', None)
        data['visitedAt'] = request.POST.get('visitedAt', None)
        data['description'] = request.POST.get('description', None)
        data['name'] = request.POST.get('name', None)
        data['floors'] = request.POST.get('floors', None)
        data['category'] = request.POST.get('category', None)

        if action == 'insert':
             return JsonResponse(building.insert(data), status=200)
        elif action == 'update':
            return JsonResponse(building.update(data), status=200)
        elif action == 'delete':
            id = kwargs.get('id', None)
            return JsonResponse(building.delete(data), status=200)
        else:            
            return JsonResponse({"ok":False,"message": "Invalid action, only 'insert', 'update' and 'delete' are allowed with POST requests!", "data":[]},status=200)
