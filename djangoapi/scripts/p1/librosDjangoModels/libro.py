from erasmus_valencia.models import Libros as LibroModel
from django.forms.models import model_to_dict

class Libro:

    def selectOne(self, data:dict) -> dict:
        try:
            libro = list(LibroModel.objects.filter(id=data['id']))[0]
            data = model_to_dict(libro)
            return {'ok':True, 'message':'Data retrieved', 'data':data}
        except Exception as e:
            return {'ok':False, 'message':str(e), 'data':[]}

    def selectAll(self) -> dict:
        try:
            libros = LibroModel.objects.all()
            data = [model_to_dict(libro) for libro in libros]
            return {'ok':True, 'message':'Data retrieved', 'data':data}
        except Exception as e:
            return {'ok':False, 'message':str(e), 'data':[]}
    
    def update(self, data:dict) -> dict:
        try:
            libro = LibroModel.objects.get(id=data['id'])
            for key, value in data.items():
                setattr(libro, key, value)
            libro.save()
            return {'ok':True, 'message':'Data updated', 'data':data}
        except Exception as e:
            return {'ok':False, 'message':str(e), 'data':[]}
        
    def insert(self, data:dict) -> dict:
        try:
            data['paginas'] = int(data['paginas'])
            data['precio'] = float(data['precio'])
            data['publicado'] = data.get('publicado', 'false').lower() == 'true'
            if data.get('precio', None) is not None and data['precio'] < 0:
                return {'ok':False, 'message':'The price cannot be negative', 'data':[]}
            if data.get('paginas', None) is not None and data['paginas'] < 0:
                return {'ok':False, 'message':'The number of pages cannot be negative', 'data':[]}
            libro = LibroModel()

            for key, value in data.items():
                setattr(libro, key, value)
            libro.save()
            return {'ok':True, 'message':'Data inserted', 'data':data}
        except Exception as e:
            return {'ok':False, 'message':str(e), 'data':[]}
    
    def delete(self, data:dict) -> dict:
        try:
            libro = LibroModel.objects.get(id=data['id'])
            libro.delete()
            return {'ok':True, 'message':'Data deleted', 'data':data}
        except Exception as e:
            return {'ok':False, 'message':str(e), 'data':[]}
        