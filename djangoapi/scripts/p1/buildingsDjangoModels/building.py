
from erasmus_valencia.models import Building as BuildingModel
from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry



class Building:


    def insert(self, data:dict) -> dict:

        try: 
            # building_model is the instance of the BuildingModel class, which is the model of the building table in the database
            # we convert our building class to the building model and then we save it to the database
            building_model = BuildingModel()
            building_model.description = data['description']
            building_model.name = data['name']
            building_model.floors = data['floors']
            building_model.height = data['height']
            building_model.category = data['category']
            building_model.visitedAt = data['visitedAt']

            # check if the geom is valid, if it is not valid return an error message
            geom = GEOSGeometry(data["geom"], srid=25830)

            if not geom.valid:
                return {
                    "ok": False,
                    "message": "Invalid geometry",
                    "data": []
                }

            building_model.geom = geom
        
            building_model.save()

            return {'ok':True, 'message':'Building inserted', 'data':[{'id':building_model.id}]}
        
        except Exception as e:

            return {'ok':False, 'message':f"An error occurred: {str(e)}", 'data':[]}


    def update(self, data:dict) -> dict:

        try:
            id= data['id']
            # get the buidlingModel instance with the id of the building we want to update
            building=list(BuildingModel.objects.filter(id=id))[0]

            # update all the data
            building.description = data['description']
            building.name = data['name']
            building.floors = data['floors']
            building.height = data['height']
            building.category = data['category']
            building.visitedAt = data['visitedAt']
            building.geom = data['geom']
            
            #building.updated_at = timezone.now()

            # save the updated building to the database
            building.save()
            return {'ok':True, 'message':'Data updated', 'data':[{'rows_updated':1}]}
        except Exception as e:
            return {'ok':False, 'message':str(e), 'data':[]}
    

    def delete(self, data:dict) -> dict:

        id = data['id']
        try:
            building = list(BuildingModel.objects.filter(id=id))[0]
            building.delete()
            return {'ok':True, 'message':'Data deleted', 'data':[{'rows_deleted':1}]}
        except Exception as e:
            return {'ok':False, 'message':str(e), 'data':[]}
    
    def select_as_dict(self, data:dict) -> dict:

        id = data['id']
        try:
            building = list(BuildingModel.objects.filter(id=id))[0]
            # the model_to_dict function is used in class
            data = model_to_dict(building)
            return {'ok':True, 'message':'Data retrieved', 'data':data}
        except Exception as e:
            return {'ok':False, 'message':str(e), 'data':[]}
    
