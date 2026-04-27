from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION
from erasmus_valencia.models import Street as StreetModel
from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection


class Street:

    def selectOne(self, data:dict) -> dict:
        '''
        Selects one street by id. this was implemented for evaluation 2 and is called in views.py
        '''
        id = data.get('id', None)
        if id is None:
            return {"ok": False, "message": "ID is required", "data": []}
        try:
            street_model = StreetModel.objects.get(id=id)
            data = model_to_dict(street_model)
            data["geom"] = street_model.geom.wkt
            return {"ok": True, "message": "Street found", "data": data}
        except StreetModel.DoesNotExist:
            return {"ok": False, "message": "Street not found", "data": []}

    def selectAll(self) -> dict:
        '''
        Selects all streets via View. This was implemented for Evalution 2 as part of the django api and is called in views.py
        '''
        try:
            street_models = StreetModel.objects.all()
            data = [model_to_dict(street_model) for street_model in street_models]

            for street in data:
                street["geom"] = street["geom"].wkt

            return {"ok": True, "message": "Streets found", "data": data}
        except Exception as e:
            return {"ok": False, "message": f"An error occurred: {str(e)}", "data": []}

    
    def _intersects(self, geom:GEOSGeometry, exclude_id: int = None) -> list:
        '''
        Checks if the geometry intersects with any other geometry in the street table. 
        If it intersects return a list of the ids of the intersecting streets, if it does not intersect return an empty list
        '''

        # get all the street models the django way without sql
        streets = StreetModel.objects.all()
        
        # if we update a street, it must be excluded from the list to avoid self comparison
        if exclude_id is not None:
            streets = streets.exclude(id=exclude_id)
        intersecting_streets = []
        for street in streets:
            if street.geom.intersects(geom):
                intersecting_streets.append(street.id)
        return intersecting_streets
    
    def _snap_to_grid(self, geom:GEOSGeometry) -> GEOSGeometry:
        '''
        Snap the geometry to a grid similiar to ST_SnapToGrid in postgis. The Code is from the profs pdf
        '''
        cursor=connection.cursor()
        query="select st_snaptogrid(st_geomfromtext(%s, %s),%s)"
        cursor.execute(query, [geom.wkt, EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])

        return GEOSGeometry(cursor.fetchall()[0][0], srid=EPSG_FOR_GEOMETRIES)

    def insert(self, data:dict) -> dict:

        '''
        Inserts a street into the database. allow_intersections is a parameter that allows to insert a street even if it intersects with another street. This is set to true by default because streets can actually intersect, but it can be set to false to prevent intersections.
        '''

        try: 
            street_model = StreetModel()
            street_model.name = data['name']
            street_model.category = data['category']
            street_model.description = data['description']
            street_model.length = data['length']
            street_model.lanes = data['lanes']
            street_model.visitedAt = data['visitedAt']

            # create the geom from wkt 
            geom = GEOSGeometry(data["geom"], srid=EPSG_FOR_GEOMETRIES)

            # snap the geometry to a grid to avoid precision issues 
            geom = self._snap_to_grid(geom)

            query = """
                SELECT id
                FROM erasmus_valencia_street    
                WHERE ST_Intersects(ST_GeomFromText(%s, %s), geom)
            """
            cursor = connection.cursor()
            cursor.execute(query, [geom.wkt, EPSG_FOR_GEOMETRIES])
            result = cursor.fetchall()

            # allow intersections is a parameter passed in the body
            allow_intersections = False
            if data.get('allow_intersections', None) is not None:
                allow_intersections = data['allow_intersections'] in ['true', 'True', 'TRUE', True]

            #intersection_list = self._intersects(geom)

            # check if the geometry intersects with any other geometry in the street table, if it does intersect ask the user if they want to insert it anyway
            # streets can actually intersect so its not an error, but we want to warn the user about it
            if len(result) > 0:

                if not allow_intersections:
                    return {
                        "ok": False,
                        "message": f"The geometry intersects with another street at id(s) {result}, insertion aborted. If you want to allow intersections, set the 'allow_intersections' parameter to true in the request body.",
                        "data": []
                    }
                
                # insert = input(f"The geometry intersects with another street at id(s) {result} Do you want to insert it anyway? (y/n)") == "y"

               #if not insert:
               #    return {
               #        "ok": False,
               #        "message": "The geometry intersects with another street, aborted by user.",
               #        "data": []
               #    }

            # check if the geom is valid, if it is not valid return an error message
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
            geom = GEOSGeometry(data["geom"], srid=EPSG_FOR_GEOMETRIES)

            geom = self._snap_to_grid(geom)

            if not geom.valid:
                return {
                    "ok": False,
                    "message": "Invalid geometry",
                    "data": []
                }

            query = """
                SELECT id
                FROM erasmus_valencia_street    
                WHERE ST_Intersects(ST_GeomFromText(%s, %s), geom) AND id <> %s
            """
            cursor = connection.cursor()
            cursor.execute(query, [geom.wkt, EPSG_FOR_GEOMETRIES, id])
            result = cursor.fetchall()

            if len(result) > 0:
                insert = input(f"The geometry intersects with another street at id(s) {result} Do you want to insert it anyway? (y/n)") == "y"

                if not insert:
                    return {
                        "ok": False,
                        "message": "The geometry intersects with another street, aborted by user.",
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