from erasmus_valencia.models import Street as StreetModel
from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry

class Street:

    def insert(self, data:dict) -> dict:



        try: 
            street_model = StreetModel()
            street_model.name = data['name']
            street_model.category = data['category']
            street_model.description = data['description']
            street_model.length = data['length']
            street_model.lanes = data['lanes']

            street_model.visitedAt = data['visitedAt']

            # check if the geom is valid, if it is not valid return an error message
            geom = GEOSGeometry(data["geom"], srid=25830)

            if not geom.valid:
                return {
                    "ok": False,
                    "message": "Invalid geometry",
                    "data": []
                }

            street_model.geom = geom
        
            street_model.save()

            return {'ok':True, 'message':'Street inserted', 'data':[{'id':street_model.id}]}
        
        except Exception as e:

            return {'ok':False, 'message':f"An error occurred: {str(e)}", 'data':[]}
    
    def update(self, data:dict) -> dict:

        try:
            id= data['id']
            # get the streetModel instance with the id of the street we want to update
            street=list(StreetModel.objects.filter(id=id))[0]

            # update all the data
            street.name = data['name']
            street.category = data['category']
            street.description = data['description']
            street.length = data['length']
            street.lanes = data['lanes']

            street.visitedAt = data['visitedAt']

            # check if the geom is valid, if it is not valid return an error message
            geom = GEOSGeometry(data["geom"], srid=25830)

            if not geom.valid:
                return {
                    "ok": False,
                    "message": "Invalid geometry",
                    "data": []
                }

            street.geom = geom
        
            street.save()

            return {'ok':True, 'message':'Street updated', 'data':[{'id':street.id}]}
        
        except Exception as e:

            return {'ok':False, 'message':f"An error occurred: {str(e)}", 'data':[]}
    
    def delete(self, data:dict) -> dict:

        id = data['id']
        try:
            street = list(StreetModel.objects.filter(id=id))[0]
            street.delete()
            return {'ok':True, 'message':'Street deleted', 'data':[{'id':id}]}
        except Exception as e:
            return {'ok':False, 'message':f"An error occurred: {str(e)}", 'data':[]}
        
    def select_as_dict(self, data:dict) -> dict:

        id = data['id']
        try:
            street = list(StreetModel.objects.filter(id=id))[0]
            street_dict = model_to_dict(street)
            street_dict['geom'] = street.geom.geojson
            return {'ok':True, 'message':'Street found', 'data':[street_dict]}
        except Exception as e:
            return {'ok':False, 'message':f"An error occurred: {str(e)}", 'data':[]}