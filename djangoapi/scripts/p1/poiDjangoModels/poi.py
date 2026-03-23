from erasmus_valencia.models import POI as POIModel
from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry

class POI:

    def insert(self, data:dict) -> dict:
        try: 
            poi_model = POIModel()
            poi_model.name = data['name']
            poi_model.description = data['description']
            poi_model.category = data['category']
            poi_model.visitedAt = data['visitedAt']

            # check if the geom is valid, if it is not valid return an error message
            geom = GEOSGeometry(data["geom"], srid=25830)

            if not geom.valid:
                return {
                    "ok": False,
                    "message": "Invalid geometry",
                    "data": []
                }

            poi_model.geom = geom
        
            poi_model.save()

            return {'ok':True, 'message':'POI inserted', 'data':[{'id':poi_model.id}]}
        
        except Exception as e:

            return {'ok':False, 'message':f"An error occurred: {str(e)}", 'data':[]}
    
    def update(self, data:dict) -> dict:
        try:
            id= data['id']
            # get the poiModel instance with the id of the poi we want to update
            poi=list(POIModel.objects.filter(id=id))[0]

            # update all the data
            poi.name = data['name']
            poi.description = data['description']
            poi.category = data['category']
            poi.visitedAt = data['visitedAt']

            # check if the geom is valid, if it is not valid return an error message
            geom = GEOSGeometry(data["geom"], srid=25830)

            if not geom.valid:
                return {
                    "ok": False,
                    "message": "Invalid geometry",
                    "data": []
                }

            poi.geom = geom
        
            poi.save()

            return {'ok':True, 'message':'POI updated', 'data':[{'id':poi.id}]}
        
        except Exception as e:

            return {'ok':False, 'message':f"An error occurred: {str(e)}", 'data':[]}
        
    
    def delete(self, data:dict) -> dict:

        id = data['id']
        try:
            poi = list(POIModel.objects.filter(id=id))[0]
            poi.delete()
            return {'ok':True, 'message':'POI deleted', 'data':[{'rows_deleted':1}]}
        except Exception as e:
            return {'ok':False, 'message':str(e), 'data':[]}
        
    def select_as_dict(self, data:dict) -> dict:

        id = data['id']
        try:
            poi = list(POIModel.objects.filter(id=id))[0]
            return {'ok':True, 'message':'POI found', 'data':[model_to_dict(poi)]}
        except Exception as e:
            return {'ok':False, 'message':str(e), 'data':[]}

