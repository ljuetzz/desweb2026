import json
from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry
from core.myLib.baseDjangoView import BaseDjangoView
from erasmus_valencia.models import Building, Street, POI


def read_json(request):
    body = request.body.decode("utf-8")
    return json.loads(body)


def building_to_dict(row):
    return {
        "id": row.id,
        "name": row.name,
        "description": row.description,
        "floors": row.floors,
        "height": row.height,
        "category": row.category,
        "visitedAt": row.visitedAt,
        "geom": row.geom.wkt
    }


def street_to_dict(row):
    return {
        "id": row.id,
        "name": row.name,
        "description": row.description,
        "length": row.length,
        "lanes": row.lanes,
        "category": row.category,
        "visitedAt": row.visitedAt,
        "geom": row.geom.wkt
    }


def poi_to_dict(row):
    return {
        "id": row.id,
        "name": row.name,
        "description": row.description,
        "category": row.category,
        "visitedAt": row.visitedAt,
        "rating": row.rating,
        "geom": row.geom.wkt
    }


class BuildingView(BaseDjangoView):

    def insert(self, request):
        try:
            data = read_json(request)
            row = Building(
                name=data["name"],
                description=data["description"],
                floors=data["floors"],
                height=data["height"],
                category=data["category"],
                visitedAt=data["visitedAt"],
                geom=GEOSGeometry(data["geom"], srid=25830)
            )
            row.save()
            return JsonResponse({"ok": True, "message": "Building inserted", "data": [building_to_dict(row)]})
        except Exception as e:
            return JsonResponse({"ok": False, "message": str(e), "data": []})

    def selectone(self, id):
        try:
            row = Building.objects.get(id=id)
            return JsonResponse({"ok": True, "message": "Building selected", "data": [building_to_dict(row)]})
        except Exception as e:
            return JsonResponse({"ok": False, "message": str(e), "data": []})

    def selectall(self):
        rows = Building.objects.all()
        data = []
        for row in rows:
            data.append(building_to_dict(row))
        return JsonResponse({"ok": True, "message": "Buildings selected", "data": data})

    def update(self, request, id):
        try:
            data = read_json(request)
            row = Building.objects.get(id=id)
            row.name = data["name"]
            row.description = data["description"]
            row.floors = data["floors"]
            row.height = data["height"]
            row.category = data["category"]
            row.visitedAt = data["visitedAt"]
            row.geom = GEOSGeometry(data["geom"], srid=25830)
            row.save()
            return JsonResponse({"ok": True, "message": "Building updated", "data": [building_to_dict(row)]})
        except Exception as e:
            return JsonResponse({"ok": False, "message": str(e), "data": []})

    def delete(self, id):
        try:
            row = Building.objects.get(id=id)
            data = building_to_dict(row)
            row.delete()
            return JsonResponse({"ok": True, "message": "Building deleted", "data": [data]})
        except Exception as e:
            return JsonResponse({"ok": False, "message": str(e), "data": []})


class StreetView(BaseDjangoView):

    def insert(self, request):
        try:
            data = read_json(request)
            row = Street(
                name=data["name"],
                description=data["description"],
                length=data["length"],
                lanes=data["lanes"],
                category=data["category"],
                visitedAt=data["visitedAt"],
                geom=GEOSGeometry(data["geom"], srid=25830)
            )
            row.save()
            return JsonResponse({"ok": True, "message": "Street inserted", "data": [street_to_dict(row)]})
        except Exception as e:
            return JsonResponse({"ok": False, "message": str(e), "data": []})

    def selectone(self, id):
        try:
            row = Street.objects.get(id=id)
            return JsonResponse({"ok": True, "message": "Street selected", "data": [street_to_dict(row)]})
        except Exception as e:
            return JsonResponse({"ok": False, "message": str(e), "data": []})

    def selectall(self):
        rows = Street.objects.all()
        data = []
        for row in rows:
            data.append(street_to_dict(row))
        return JsonResponse({"ok": True, "message": "Streets selected", "data": data})

    def update(self, request, id):
        try:
            data = read_json(request)
            row = Street.objects.get(id=id)
            row.name = data["name"]
            row.description = data["description"]
            row.length = data["length"]
            row.lanes = data["lanes"]
            row.category = data["category"]
            row.visitedAt = data["visitedAt"]
            row.geom = GEOSGeometry(data["geom"], srid=25830)
            row.save()
            return JsonResponse({"ok": True, "message": "Street updated", "data": [street_to_dict(row)]})
        except Exception as e:
            return JsonResponse({"ok": False, "message": str(e), "data": []})

    def delete(self, id):
        try:
            row = Street.objects.get(id=id)
            data = street_to_dict(row)
            row.delete()
            return JsonResponse({"ok": True, "message": "Street deleted", "data": [data]})
        except Exception as e:
            return JsonResponse({"ok": False, "message": str(e), "data": []})


class PoiView(BaseDjangoView):

    def insert(self, request):
        try:
            data = read_json(request)
            row = POI(
                name=data["name"],
                description=data["description"],
                category=data["category"],
                visitedAt=data["visitedAt"],
                rating=data["rating"],
                geom=GEOSGeometry(data["geom"], srid=25830)
            )
            row.save()
            return JsonResponse({"ok": True, "message": "POI inserted", "data": [poi_to_dict(row)]})
        except Exception as e:
            return JsonResponse({"ok": False, "message": str(e), "data": []})

    def selectone(self, id):
        try:
            row = POI.objects.get(id=id)
            return JsonResponse({"ok": True, "message": "POI selected", "data": [poi_to_dict(row)]})
        except Exception as e:
            return JsonResponse({"ok": False, "message": str(e), "data": []})

    def selectall(self):
        rows = POI.objects.all()
        data = []
        for row in rows:
            data.append(poi_to_dict(row))
        return JsonResponse({"ok": True, "message": "POIs selected", "data": data})

    def update(self, request, id):
        try:
            data = read_json(request)
            row = POI.objects.get(id=id)
            row.name = data["name"]
            row.description = data["description"]
            row.category = data["category"]
            row.visitedAt = data["visitedAt"]
            row.rating = data["rating"]
            row.geom = GEOSGeometry(data["geom"], srid=25830)
            row.save()
            return JsonResponse({"ok": True, "message": "POI updated", "data": [poi_to_dict(row)]})
        except Exception as e:
            return JsonResponse({"ok": False, "message": str(e), "data": []})

    def delete(self, id):
        try:
            row = POI.objects.get(id=id)
            data = poi_to_dict(row)
            row.delete()
            return JsonResponse({"ok": True, "message": "POI deleted", "data": [data]})
        except Exception as e:
            return JsonResponse({"ok": False, "message": str(e), "data": []})