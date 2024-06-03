from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Advocate
from .serializer import AdvocateSerializer
from django.db.models import Q
from rest_framework.views import APIView



# ?format=json  ==============> this is something you can use in the end of the url



#accepted_renderer not set on Response
@api_view(['GET'])
def endpoints(request):
  data=['/advocates','advocates/:username']
  return Response(data) # in jsonResponse to let the non-dict obj to be serialized, set the safe go be falsed

@api_view(['GET','POST'])
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
