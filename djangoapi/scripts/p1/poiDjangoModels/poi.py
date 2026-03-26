from django.db import connection

from erasmus_valencia.models import POI as POIModel
from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry
from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION


class POI:


    def _check_identical(self, geom:GEOSGeometry, exclude_id: int = None) -> bool:

        '''
        Checks if the geometry is identical to any other geometry in the poi table.
        This has to be done after snap_to_grid!
        '''
        
        # get all the pois the django way without sql
        pois = POIModel.objects.all()

        # if we update a poi, it must be excluded from the list to avoid self comparison
        if exclude_id is not None:
            pois = pois.exclude(id=exclude_id)

        # check for each point wether the geometry is identical. This has to be done after snap_to_grid
        for poi in pois:
            if poi.geom.equals(geom):
                return True
        return False

    def _snap_to_grid(self, geom:GEOSGeometry) -> GEOSGeometry:
        '''
        Snap the geometry to a grid similiar to ST_SnapToGrid in postgis. The Code is from the profs pdf
        '''
        cursor=connection.cursor()
        query="select st_snaptogrid(st_geomfromtext(%s, %s),%s)"
        cursor.execute(query, [geom.wkt, EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])

        return GEOSGeometry(cursor.fetchall()[0][0], srid=EPSG_FOR_GEOMETRIES)
    
    def insert(self, data:dict) -> dict:
        try: 
            poi_model = POIModel()
            poi_model.name = data['name']
            poi_model.description = data['description']
            poi_model.category = data['category']
            poi_model.visitedAt = data['visitedAt']

            # check if the geom is valid, if it is not valid return an error message
            geom = GEOSGeometry(data["geom"], srid=EPSG_FOR_GEOMETRIES)

            # snap to grid to avoid precision issues that can cause the geometry to be invalid or to intersect with other geometries
            geom = self._snap_to_grid(geom)

            if not geom.valid:
                return {
                    "ok": False,
                    "message": "Invalid geometry",
                    "data": []
                }
            
            # to see wether the poi is inside a building we run this query
            query = """
                SELECT 1
                FROM erasmus_valencia_building
                WHERE ST_Intersects(geom, ST_GeomFromText(%s, %s))
            """
            cursor = connection.cursor()
            cursor.execute(query, [geom.wkt, EPSG_FOR_GEOMETRIES])
            
            if cursor.fetchone() is None:
                # ask the user if he really wants to insert a point outside of buildings
                if input("The Point is not located within any building. Do you want to insert it anyway? (y/n)") != "y":
                    return {
                        "ok": False,
                        "message": "The Point is not located within any building, aborted by user",
                        "data": []
                    }

            
            if self._check_identical(geom):
                return {
                    "ok": False,
                    "message": "The Point is identical to another geometry in the poi table: The same point already exists!",
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
            geom = GEOSGeometry(data["geom"], srid=EPSG_FOR_GEOMETRIES)

            geom = self._snap_to_grid(geom)

            if not geom.valid:
                return {
                    "ok": False,
                    "message": "Invalid geometry",
                    "data": []
                }
            
            if self._check_identical(geom, exclude_id=id):
                return {
                    "ok": False,
                    "message": "The Point is identical to another geometry in the poi table: The same point already exists!",
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

