from django.urls import path
from .views import *

urlpatterns = [

    path('', endpoints),
    path('advocates/',advocates_list),
  #  path('advocates/<str:username>',advocates_detail)
    path('advocates/<str:username>',AdvocateDetail.as_view()),
    path('companies/', companies_list)
    

]

