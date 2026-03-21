# geodajango for geometry!!! 
from django.contrib.gis.db import models
#from django.db import models
#from django.utils import timezone


# Create your models here.

class POI(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    visitedAt = models.DateTimeField()
    geom = models.PointField(srid=25830)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
class Street(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    length = models.FloatField()
    category = models.CharField(max_length=100)
    visitedAt = models.DateTimeField()
    geom = models.LineStringField(srid=25830)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.name

class Building(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    floors = models.IntegerField()
    height = models.FloatField()
    category = models.CharField(max_length=100)
    visitedAt = models.DateTimeField()
    geom = models.PolygonField(srid=25830)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.name