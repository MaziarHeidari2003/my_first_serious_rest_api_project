from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('', endpoints),
    path('advocates/',advocates_list),
  #  path('advocates/<str:username>',advocates_detail)
    path('advocates/<str:username>',AdvocateDetail.as_view()),
    path('companies/', companies_list),
     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    

]

