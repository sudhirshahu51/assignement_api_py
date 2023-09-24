
from django.urls import path
from . import views

urlpatterns = [
    path('', views.AssigneApi.as_view(), name='index'),
    path('auth/', views.Auth.as_view(), name='auth'),
   #path('auth/', Auth.as_view(), name='auth'),
    path('country/<str:country>/', views.CountryDetail.as_view(), name='country-detail'),
    path('countries/', views.CountryList.as_view(), name='country-list'),
    path('data/countries/page/<int:page>/', views.CountryList.as_view(), name='country-list-paginated'),
]



