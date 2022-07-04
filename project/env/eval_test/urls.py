#   DJANGO IMPORTS
from django.urls import path, include
#   REST FRAMEWORK IMPORTS
from rest_framework import routers
#   APP IMPORTS
from .views import PokemonViewSet, PokemonStorage, PokemonEdit, PokemonParty,PokemonSwap, RegionsGeneral, RegionsLocations, LocationDetail,AreaDetail, Login


route = routers.DefaultRouter()
#route.register(r'pokemons/<int:pk>', PokemonViewSet)

#   CUSTOM ENDPOINTS
urlpatterns = path('login/',Login.as_view()),
urlpatterns += path('pokemons/<int:pk>/', PokemonViewSet.as_view()),
urlpatterns += path('pokemons/own/', PokemonStorage.as_view()),
urlpatterns += path('pokemons/own/<int:pk>/', PokemonEdit.as_view()),
urlpatterns += path('pokemons/own/party/', PokemonParty.as_view()),
urlpatterns += path('pokemons/own/swap/', PokemonSwap.as_view()),
urlpatterns += path('regions/', RegionsGeneral.as_view()),
urlpatterns += path('regions/<int:pk>/', RegionsLocations.as_view()),
urlpatterns += path('location/<int:pk>/', LocationDetail.as_view()),
urlpatterns += path('areas/<int:pk>/', AreaDetail.as_view()),
urlpatterns += path('', include(route.urls)),