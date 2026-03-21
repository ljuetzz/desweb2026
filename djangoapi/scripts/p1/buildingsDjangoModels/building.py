
from erasmus_valencia.models import Building as BuildingModel

class Building:

    def insert(self, data:dict) -> dict:

        building = BuildingModel()
        building.description = data['description']
        building.name = data['name']
        building.floors = data['floors']
        building.height = data['height']
        building.category = data['category']
        building.visitedAt = data['visitedAt']
        building.geom = data['geom']
    
        building.save()

        return {'ok':True, 'message':'Building inserted', 'data':[{'id':building.id}]}

    #ef update(self, d):
    #   id=d['id']
    #   b=list(BuildingsModel.objects.filter(id=id))[0]
    #   b.description = d[’description’]
    #   ....
    #   b.save()
    #   {ok:true, message: Data updated, data:[{rows_updated
    #   :1}]}