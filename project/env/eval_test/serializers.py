from rest_framework_json_api import serializers
from eval_test.models import Pokemon, UserPokemon, Region, Locations, Available
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','email')

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','password')
        extra_kwargs = {'password': {'write_only': True}}

        def get(self,validated_data):
            user = User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'])
            return user


class PokemonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pokemon
        fields = ('id','abilities', 'capture_rate', 'color', 'flavor_text', 'height', 'moves', 'name','sprites','stats','types','weight')

class UserPokemonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserPokemon
        fields = ('id','nick_name','is_party_member','specie_id','user_id')

class RegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = ('id','name','locations')

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Locations
        fields = ('id','name','areas','regions','pokemons')

class AvailableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Available
        fields = ('id','name','pokemons','location')
