# Create your views here.

#Importing required modules
from django.http import HttpResponse
import requests
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import *
from django.http import HttpResponse, JsonResponse
from .serializers import CountrySerializer
from rest_framework import status
import logging

timeout = 5
# Create your views here.
logger = logging.getLogger('assignement_api')

class ResponseFunctions:
    @staticmethod
    def returnResponse(result):
        try:
            return HttpResponse(JsonResponse(result, safe=False), content_type='application/json')
        except Exception as ex:
            logger.exception(ex)
            return HttpResponse(JsonResponse(result, safe=False), content_type='application/json')
        
@method_decorator(csrf_exempt, name='dispatch')
class AssigneApi(APIView): #Used for testing the server.
    
    def get(self, request):
        logger.info("Testing: End-point is OK")
        result = {'data': "Testing: End-point is OK"}
        return ResponseFunctions.returnResponse(result)
            #return HttpResponse(JsonResponse(result, safe=False), content_type='application/json')    

class Auth(APIView): #Authentication API Class
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # Validating the credentials(Hard coded as asked with defination of username and password)
        if username == "123" and password == "12345":
            user, created = User.objects.get_or_create(username=username)
            token, created = Token.objects.get_or_create(user=user)  # Create or get the token
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class CountryDetail(APIView): #Country API Class for detailed info about country
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def get(self, request, country):
        error = ""
        country_response = {'errorCode': 'failure', 'country_info': "", 'errorMsg': 'Failed to retrive country info','country' : country, "error": error}
        logger.info("Country data request received")
        
        #Using 
        if request.method == "GET":
            logger.info('Request received to retrive detailed info. of specific country: {}'.format(country))
            country_response = self.country_details(country)   
        return ResponseFunctions.returnResponse(country_response)
    

    def country_details(self,country):
        """Fetch detailed information about a specific country by 
        providing its name as a parameter
        Keyword Arguments:
            country -- Name of country
        Returns: 
            country_response: Json containing detailed info about 
            errorcode, countrydata, errorMsg and country. 
        """
        logger.info("Inside country_info retrivel function")
        data = {}
        country_response = {'errorCode': 'failure', 'country_info': data, 'errorMsg': 'Failed to retrive country info','country' : country, "error": ""}         
        #Code to request Api for the country data.
        #country = "india"
        try:
            url = "https://restcountries.com/v3.1/name/" + str(country)
            request_data=requests.get(url = url, timeout = timeout, verify = True)
            request_data.raise_for_status()
            logger.info("Sucessfully retrived country data.")
            data = request_data.json()
            country_response = {'errorCode': 'Success', 'country_info': data, 'errorMsg': 'Successful to retrive country info', 'country' : country, "error":"none" } 
        except requests.exceptions.RequestException as e: 
            logger.exception("Failed to retrive country information for {} with request error {}".format(country, e))
            country_response = {'errorCode': 'failure', 'country_info': data, 'errorMsg': 'Failed to retrive country info','country' : country, "error": str(e)} 
            #raise SystemExit(e)
        except Exception as e: #Too handle exceptions other than request.
            logger.exception("Failed to retrive country information with error {}".format(e))
            country_response = {'errorCode': 'failure', 'country_info': data, 'errorMsg': 'Failed to retrive country info','country' : country, "error": str(e)} 
        return country_response
    

class CountryList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
            response = {}
            logger.info("Country list request received")
            #authentication_classes = [TokenAuthentication]
            #permission_classes = [IsAuthenticated]

            #Capturing the Data in Json format
            if request.method == "GET":
                logger.info('Request received to retrieve a list of all countries names based'
                            ' on filters (population/area/language) and sorting(asc/desc)')
                response = self.countries_list(request)    
            return response
    
    def countries_list(self, request):  
      #Use request to retrive data froom countries_api, use pagination
        """Retrieve a list of all countries' names based on filters 
        (population/area/language) and sorting(asc/desc)
        Keyword Arguments:
            param filters - a list of fields to filter the output of the request to include only the specified fields.
        Returns:
        either a Country object or a list of Countries """
        logger.info("Inside countries_list function") 
        countries_response = {'errorCode': 'failure', 'errorMsg': 'Failed to retrive country info', "error": ""}         
    

         # Get query parameters from the request
        logger.info("parameters {}".format(request.query_params.dict()))
        filters = request.query_params.dict()
        sort_by = filters.pop('sort_by', None)
        sort_order = filters.pop('sort_order', 'asc')
        page = request.query_params.get('page')
        page_size = request.query_params.get('page_size')
        
        # Query the REST Countries API
        try:
            response = requests.get('https://restcountries.com/v3.1/all')
            response.raise_for_status()
            countries_data = response.json()

            # Apply filters
            filtered_countries = countries_data
            for key, value in filters.items():
                if key in ['population', 'area']:
                    # Give list of countries with Population or area than the provided filter value 
                    filtered_countries = [country for country in filtered_countries if
                                          country.get(key) and country[key] >= float(value)]
                elif key == 'language':
                    filtered_countries = [country for country in filtered_countries if
                                          country.get('languages') and (value.lower() in [lang.lower() for lang in country['languages'].values()])]
                elif key in ["page", "page_size"]:
                    pass   
                else:
                    countries_response = {'errorCode': 'failure', 'errorMsg': 'Failed to retrive countrylist', "error": 'Invalid filter key: {}'.format(key)}
                    return Response(countries_response, status=status.HTTP_400_BAD_REQUEST)

        # Sort the filtered countries
            if sort_by:
                if sort_by == 'name':
                    filtered_countries.sort(key=lambda x: x.get('name', '').lower() if isinstance(x.get('name', ''), str) else '')
                    #filtered_countries.sort(key=lambda x: x.get('name', '').lower())
                elif sort_by in ['population', 'area']:
                    filtered_countries.sort(key=lambda x: x.get(sort_by, 0))
                else:
                    countries_response = {'errorCode': 'failure', 'errorMsg': 'Failed to retrive countries data', "error": "Invalid Sort Key: {}".format(sort_by)}
                    return Response(countries_response, status=status.HTTP_400_BAD_REQUEST)

            # Apply sort order
            if sort_order == 'desc':
                filtered_countries.reverse()

            # Extract country names from the filtered and sorted list
            country_names = [country['name']['common'] for country in filtered_countries]
            logger.info("Sucessfully generated the list of counties {}".format(country_names))

        

            # Apply paginat
            paginator = PageNumberPagination()
            paginator.page_size = int(page_size) if page_size else 10  # Set a default page size if not provided
            result_page = paginator.paginate_queryset(country_names, request)
            logger.info("started pagination")
            return paginator.get_paginated_response(result_page)

            #return Response({'country_names': country_names}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            countries_response = {'errorCode': 'failure', 'errorMsg': 'Failed to retrive countries data', "error": str(e)}
            return Response(countries_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



        








    #Write code for filter part from here.
    