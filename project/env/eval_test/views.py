#   DJANGO IMPORTS
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

#   REST FRAMEWORK IMPORTS
from rest_framework.decorators import api_view, action, parser_classes, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status,viewsets,generics
from rest_framework.response import Response

#   APP MODEL IMPORTS
from eval_test.models import Pokemon, UserPokemon, Region, Locations, Available
#   APP SERIALIZER IMPORTS
from eval_test.serializers import PokemonSerializer, UserPokemonSerializer, RegionSerializer, LocationSerializer, AvailableSerializer,LoginSerializer

#   UTILS IMPORTS
import json, random

# MAX ITEMS IN PARTY
MAX_PARTY_ITEMS = 6

#   String to boolean function
def toBool(x):
    return x in ("True","true",True)

#   LOGIN HANDLERS
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        serializer_class = LoginSerializer
        username = request.data['username']
        password = request.data['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Invalid User'})

        pwd_valid = check_password(password, user.password)
        if not pwd_valid:
            return Response({'error': 'Invalid Password'})

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

#   POKEMON HANDLER
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
class PokemonViewSet(generics.GenericAPIView):
    serializer_class = PokemonSerializer

    def get(self, request,pk):
        serializer_class = PokemonSerializer

        try:
            pokemon = Pokemon.objects.filter(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Invalid Pokemon'})
        serialized_obj = serializers.serialize('json', pokemon)

        for item in json.loads(serialized_obj):
            abs = set()
            for it in json.loads(item['fields']['abilities']):
                abs.add(it)
            moves = set()
            for it in json.loads(item['fields']['moves']):
                moves.add(it)
            types = set()
            for it in json.loads(item['fields']['types']):
                types.add(it)
            result={
                'id': pk,
                'abilities': abs,
                'capture_rate': item['fields']['capture_rate'],
                'color': item['fields']['color'],
                'flavor_text': item['fields']['flavor_text'],
                'height': item['fields']['height'],
                'moves': moves,
                'name': [item['fields']['name']],
                'sprites': Pokemon.objects.get(id=pk).sprites,
                'stats':item['fields']['stats'],
                'types':types,
                'weight':item['fields']['weight']
            }
        return Response(result)

#   POKEMON OWN
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
class PokemonStorage(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPokemonSerializer
    def get(self,request):
        serializer_class = UserPokemonSerializer
        try:
            token_key = request.headers['authorization'].replace('Token ', '')
        except:
            return Response({'error':'Authorization required'})

        try:
            userpokemon = UserPokemon.objects.filter(user_id=Token.objects.get(key=token_key).user_id)
        except User.DoesNotExist:
            return Response({'error':'Invalid User'})
        serialized_obj = serializers.serialize('json', userpokemon)

        result = []
        for item in json.loads(serialized_obj):
            result.append({
                'id': item['pk'],
                'nick_name': item['fields']['nick_name'],
                'is_party_member': item['fields']['is_party_member'],
                'specie': {
                    'id': Pokemon.objects.get(id=item['fields']['specie']).id,
                    'name': Pokemon.objects.get(id=item['fields']['specie']).name,
                    'sprites': Pokemon.objects.get(id=item['fields']['specie']).sprites
                },
            })
        return Response(result)

    def post(self,request):
        serializer_class = UserPokemonSerializer
        try:
            token_key=request.headers['authorization'].replace('Token ','')
        except:
            return Response({'error':'Authorization required'})

        specie = request.data['specie']
        nick_name = request.data['nick_name']
        is_party_member = toBool(request.data['is_party_member'])

        try:
            userpokemon = UserPokemon.objects.filter(user_id=Token.objects.get(key=token_key).user_id, is_party_member=True)
        except User.DoesNotExist:
            return Response({'error':'Invalid User'})

        if len(userpokemon) == MAX_PARTY_ITEMS and is_party_member == True:
            return Response({'error':'Party Members are complete'})
        if len(UserPokemon.objects.filter(user_id=Token.objects.get(key=token_key).user_id, nick_name=nick_name)) > 0:
            return Response({'error':'Nick Name already exists'})

        userpoke = UserPokemon(nick_name=nick_name, is_party_member=is_party_member, specie_id=specie,
                               user_id=Token.objects.get(key=token_key).user_id)

        if random.SystemRandom().random() > Pokemon.objects.get(pk=request.data['specie']).capture_rate/100:
            result = {'detail':'Could not capture',
                      'pokemon': Pokemon.objects.get(pk=request.data['specie']).name}
            return Response(result, status=status.HTTP_200_OK)
        else:
            userpoke.save()
        lastpoke = json.loads(serializers.serialize('json', [UserPokemon.objects.last()]))
        result = {
            'id': lastpoke[0]['pk'],
            'nick_name': lastpoke[0]['fields']['nick_name'],
            'is_party_member': lastpoke[0]['fields']['is_party_member'],
            'specie': lastpoke[0]['fields']['specie']
        }
        return Response(result, status=status.HTTP_201_CREATED)

#   POKEMON EDIT NICK NAME
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
class PokemonEdit(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPokemonSerializer

    def put(self,request,pk):
        serializer_class = UserPokemonSerializer
        try:
            token_key = request.headers['authorization'].replace('Token ', '')
        except:
            return Response({'error':'Authorization required'})

        nick_name = request.data['nick_name']

        try:
            userpokemon = UserPokemon.objects.get(user_id=Token.objects.get(key=token_key).user_id,pk=pk)
        except User.DoesNotExist:
            return Response({'error':'Invalid User'})

        # serialized_obj = serializers.serialize('json', userpokemon)

        userpokemon.nick_name = nick_name
        userpokemon.save()

        lastpoke = json.loads(serializers.serialize('json', [UserPokemon.objects.get(user_id=Token.objects.get(key=token_key).user_id,pk=pk)]))
        result = {
            'id': lastpoke[0]['pk'],
            'nick_name': lastpoke[0]['fields']['nick_name'],
            'is_party_member': lastpoke[0]['fields']['is_party_member'],
            'specie': lastpoke[0]['fields']['specie']
        }
        return Response(result, status=status.HTTP_200_OK)

    def patch(self,request,pk):
        serializer_class = UserPokemonSerializer
        try:
            token_key = request.headers['authorization'].replace('Token ', '')
        except:
            return Response({'error':'Authorization required'})

        nick_name = request.data['nick_name']

        try:
            userpokemon = UserPokemon.objects.get(user_id=Token.objects.get(key=token_key).user_id,pk=pk)
        except User.DoesNotExist:
            return Response({'error':'Invalid User'})

        # serialized_obj = serializers.serialize('json', userpokemon)

        userpokemon.nick_name = nick_name
        userpokemon.save()

        lastpoke = json.loads(serializers.serialize('json', [UserPokemon.objects.get(user_id=Token.objects.get(key=token_key).user_id,pk=pk)]))
        result = {
            'id': lastpoke[0]['pk'],
            'nick_name': lastpoke[0]['fields']['nick_name'],
            'is_party_member': lastpoke[0]['fields']['is_party_member'],
            'specie': lastpoke[0]['fields']['specie']
        }
        return Response(result, status=status.HTTP_200_OK)

    def delete(self,request,pk):
        serializer_class = UserPokemonSerializer
        try:
            token_key = request.headers['authorization'].replace('Token ', '')
        except:
            return Response({'error':'Authorization required'})

        try:
            userpokemon = UserPokemon.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error':'Invalid User'})

        userpokemon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#   POKEMON PARTY
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
class PokemonParty(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPokemonSerializer
    def get(self,request):
        serializer_class = UserPokemonSerializer
        try:
            token_key = request.headers['authorization'].replace('Token ', '')
        except:
            return Response({'error':'Authorization required'})

        try:
            userpokemon = UserPokemon.objects.filter(user_id=Token.objects.get(key=token_key).user_id,is_party_member=True)
        except User.DoesNotExist:
            return Response({'error':'Invalid User'})
        serialized_obj = serializers.serialize('json', userpokemon)

        result = []
        for item in json.loads(serialized_obj):
            result.append({
                'id': item['pk'],
                'nick_name': item['fields']['nick_name'],
                'is_party_member': item['fields']['is_party_member'],
                'specie': {
                    'id': Pokemon.objects.get(id=item['fields']['specie']).id,
                    'name': Pokemon.objects.get(id=item['fields']['specie']).name,
                    'sprites': Pokemon.objects.get(id=item['fields']['specie']).sprites
                },
            })
        return Response(result)

#   POKEMON SWAP PARTY
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
class PokemonSwap(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPokemonSerializer
    def post(self,request):
        serializer_class = UserPokemonSerializer
        try:
            token_key = request.headers['authorization'].replace('Token ', '')
        except:
            return Response({'error':'Authorization required'})

        entering_the_party = request.data['entering_the_party']
        leaving_the_party = request.data['leaving_the_party']

        userpokemon = UserPokemon.objects.filter(user_id=Token.objects.get(key=token_key).user_id, is_party_member=True)

        if len(userpokemon) == MAX_PARTY_ITEMS:
            if leaving_the_party != None:
                #   Leaving the party
                userpokemon = UserPokemon.objects.get(user_id=Token.objects.get(key=token_key).user_id,
                                                      pk=leaving_the_party)
                userpokemon.is_party_member = False
                userpokemon.save()

                #   Entering the party
                if entering_the_party != None:
                    userpokemon = UserPokemon.objects.get(user_id=Token.objects.get(key=token_key).user_id,
                                                          pk=entering_the_party)
                    userpokemon.is_party_member = True
                    userpokemon.save()

            else:
                if entering_the_party == None and leaving_the_party == None:
                    return Response({'error': 'Null values'})
                else:
                    return Response({'error': 'Party Members are complete'})
        else:
            #   Entering the party
            if entering_the_party != None:
                userpokemon = UserPokemon.objects.get(user_id=Token.objects.get(key=token_key).user_id,
                                                      pk=entering_the_party)
                userpokemon.is_party_member = True
                userpokemon.save()


            #   Leaving the party
            if leaving_the_party != None:
                userpokemon = UserPokemon.objects.get(user_id=Token.objects.get(key=token_key).user_id,
                                                      pk=leaving_the_party)
                userpokemon.is_party_member = False
                userpokemon.save()


        userpokemon = UserPokemon.objects.filter(user_id=Token.objects.get(key=token_key).user_id, is_party_member=True)
        serialized_obj = serializers.serialize('json', userpokemon)

        result = []
        for item in json.loads(serialized_obj):
            result.append({
                'id': item['pk'],
                'nick_name': item['fields']['nick_name'],
                'is_party_member': item['fields']['is_party_member'],
                'specie': {
                    'id': Pokemon.objects.get(id=item['fields']['specie']).id,
                    'name': Pokemon.objects.get(id=item['fields']['specie']).name,
                    'sprites': Pokemon.objects.get(id=item['fields']['specie']).sprites
                },
            })
        return Response(result)

#   REGION HANDLER
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
class RegionsGeneral(generics.GenericAPIView):
    serializer_class = RegionSerializer

    def get(self, request):
        serializer_class = RegionSerializer

        regions = Region.objects.all()
        serialized_obj = serializers.serialize('json', regions)

        result = []
        for item in json.loads(serialized_obj):
            result.append({
                'id': item['pk'],
                'name': item['fields']['name']})
        return Response(result)

#   REGION LOCATIONS HANDLER
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
class RegionsLocations(generics.GenericAPIView):
    serializer_class = RegionSerializer

    def get(self, request,pk):
        serializer_class = RegionSerializer

        regions = Region.objects.filter(pk=pk)
        serialized_obj = serializers.serialize('json', regions)


        for item in json.loads(serialized_obj):
            locs = []
            cnt = 0
            for loc in json.loads(item['fields']['locations']):
                cnt += 1
                locs.append({
                    'id':cnt,
                    'name':loc
                })
            result = {
                'id': item['pk'],
                'locations': locs,
                'name': item['fields']['name']
            }
        return Response(result)

#   LOCATION HANDLER
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
class LocationDetail(generics.GenericAPIView):
    serializer_class = LocationSerializer

    def get(self, request,pk):
        serializer_class = LocationSerializer

        locations = Locations.objects.filter(pk=pk)
        serialized_obj = serializers.serialize('json', locations)

        for item in json.loads(serialized_obj):
            locs = []
            cnt = 0
            #
            for loc in json.loads(item['fields']['areas']):
                cnt += 1
                availables = Available.objects.filter(name=loc)
                locs.append({
                    'id':cnt,
                    'name':loc,
                    'pokemon_count':len(json.loads(serializers.serialize('json', availables))),
                    'location':pk
                })
            result = {
                'id': item['pk'],
                'areas': locs,
                'name': item['fields']['name'],
                'region':Region.objects.get(name=Locations.objects.get(name=item['fields']['name']).region).id
            }
        return Response(result)

#   AREA HANDLER
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
class AreaDetail(generics.GenericAPIView):
    serializer_class = AvailableSerializer

    def get(self, request,pk):
        serializer_class = AvailableSerializer

        availables = Available.objects.filter(pk=pk)
        serialized_obj = serializers.serialize('json', availables)

        for item in json.loads(serialized_obj):
            pokes = []
            cnt = 0
            for poke in json.loads(item['fields']['pokemons']):
                cnt += 1
                pokes.append({
                    'id':Pokemon.objects.get(name=poke.capitalize()).id,
                    'name':Pokemon.objects.get(name=poke.capitalize()).name,
                    'sprites':Pokemon.objects.get(name=poke.capitalize()).sprites
                })
            result = {
                'id':pk,
                'pokemon_count': len(json.loads(item['fields']['pokemons'])),
                'pokemons': pokes,
                'name': item['fields']['name'],
                'location':Locations.objects.get(name=item['fields']['location']).id
            }
        return Response(result)

