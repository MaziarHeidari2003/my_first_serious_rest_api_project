from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Advocate,Company
from .serializer import AdvocateSerializer,CompanySerializer
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes




# ?format=json  ==============> this is something you can use in the end of the url



#accepted_renderer not set on Response
@api_view(['GET'])
def endpoints(request):
  data=['/advocates','advocates/:username']
  return Response(data) # in jsonResponse to let the non-dict obj to be serialized, set the safe go be falsed

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def advocates_list(request):
  if request.method == 'GET':

    query = request.GET.get('query')
    if query == None:
      query = ''

    advocates = Advocate.objects.filter(Q(username__icontains=query)| Q(bio__icontains=query))
    serializer = AdvocateSerializer(advocates, many=True)
    return Response(serializer.data)
  
  if request.method == 'POST':
    advocate=Advocate.objects.create(
      username=request.data['username'],
      bio= request.data['bio']
    )
    serializer = AdvocateSerializer(advocate)
    return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
def advocates_detail(request,username):
  advocate = Advocate.objects.get(username=username)

  if request.method == 'GET':
    serializer = AdvocateSerializer(advocate)
    return Response(serializer.data)

  if request.method == 'PUT':
    advocate.username=request.data['username']
    advocate.bio=request.data['bio']
    advocate.save()
    serializer = AdvocateSerializer(advocate)
    return Response(serializer.data)

  if request.method == 'DELETE':
    advocate.delete()
    return Response('advocate was deleted')

class AdvocateDetail(APIView):
  def get_object(self,username):
    try:
      return Advocate.objects.get(username=username)
    except Advocate.DoesNotExist:
      raise JsonResponse("Advocate doesnt exist")
    
  def get(self,request,username):
    advocate = self.get_object(username)
    serializer = AdvocateSerializer(advocate,many=False)
    return Response(serializer.data)
  
  def put(self,request,username):
    advocate = self.get_object(username)
    advocate.bio = request.data['bio']
    advocate.username= request.data['username']
    serializer = AdvocateSerializer(advocate)
    return Response(serializer.data)
  
  def delete(self,request,username):
    advocate = self.get_object(username)
    advocate.delete()
    return Response('advocate was deleted')

@api_view(['GET'])
def companies_list(request):
  companies = Company.objects.all()
  serializer = CompanySerializer(companies,many=True)
  return Response(serializer.data)









"""
steps for authentication 
1 => pip install djangorestframework-simplejwt
2 => 

REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )


    3 =>
in veiws

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
and add the  @permission_classes([IsAuthenticated]) to the target view


4=> 
lets use postman

5 =>
lets do some imports in urls.py 

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

in urls.py
     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

     now you can generate tokens
     so go back to postman and check this out


     6 =>
     you want to customize anthing such as expire time?


     SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=20),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY":SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
 

"""