#   DJANGO IMPORTS
from django.contrib import admin
#   APP IMPORTS
from .models import Pokemon, UserPokemon, Available, Locations, Region

#   ADMIN MODELS
admin.site.register(Pokemon)
admin.site.register(UserPokemon)
admin.site.register(Available)
admin.site.register(Locations)
admin.site.register(Region)