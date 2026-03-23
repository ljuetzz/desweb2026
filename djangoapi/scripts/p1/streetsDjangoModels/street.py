from erasmus_valencia.models import Street as StreetModel
from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry

class Street:

    def insert(self, data:dict) -> dict:

        try: 
            street_model = StreetModel()
            street_model.name = data['name']
            street_model.category = data['category']
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