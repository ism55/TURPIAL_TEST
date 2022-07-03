#   DJANGO IMPORTS
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User

#   POKEMON MODEL
class Pokemon(models.Model):
    abilities = ArrayField(models.CharField(max_length=200, blank=True, null=True), default= list)
    capture_rate = models.IntegerField()
    color = models.CharField(max_length=200, blank=True, null=True, default="")
    flavor_text = models.CharField(max_length=1000, blank=True, null=True, default="")
    height = models.IntegerField()
    moves = ArrayField(models.CharField(max_length=200, blank=True, null=True), default= list)
    name = models.CharField(max_length=200, blank=True, null=True, default="")
    sprites = models.JSONField()
    stats = models.JSONField()
    types = ArrayField(models.CharField(max_length=200, blank=True, null=True), default= list)
    weight = models.IntegerField()
    def __str__(self):
        return self.name

#   USER POKEMON DATABASE MODEL
class UserPokemon(models.Model):
    nick_name = models.CharField(max_length=200, blank=False, null=False, default="Rambo")
    is_party_member = models.BooleanField(default=False)
    specie = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)

#   REGION DATABASE MODEL
class Region(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, default="Region")
    locations = ArrayField(models.CharField(max_length=200, blank=True, null=True), default= list)
    def __str__(self):
        return str(self.name)

#   LOCATIONS DATABASE MODEL
class Locations(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, default="Location")
    areas = ArrayField(models.CharField(max_length=200, blank=True, null=True), default= list)
    region = models.CharField(max_length=200, blank=False, null=False, default="Region")
    areas = ArrayField(models.CharField(max_length=200, blank=True, null=True ), default=list)
    def __str__(self):
        return str(self.name)

#   AVAILABLE POKEMONS DATABASE MODEL
class Available(models.Model):
    location = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    pokemons = ArrayField(models.CharField(max_length=200, blank=True, null=True), default= list)
    def __str__(self):
        return str(self.name)