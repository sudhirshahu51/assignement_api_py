from rest_framework import permissions
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework_api_key.models import APIKey
from rest_framework.exceptions import APIException
import logging

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger('assignement_api')
class HasAPIAccess(permissions.BasePermission):
    # message = 'Invalid or missing API Key.'
    response = {}
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_API_KEY', '')

        if not api_key:
            logger.error("Forbidden access, api key not provided.")
            response = {'status': 403, 'message': "Forbidden access, api key not provided." }
            raise exceptions.NotFound(response)
        try:
            permission = APIKey.objects.filter(key=api_key).exists()

            if not permission:
                logger.error("Unauthorized access, no user found with the access key.")
                response = {'status': 401, 'message': "Unauthorized access, no user found with the access key." }
                raise exceptions.AuthenticationFailed(response)
                return False
            else:
                return True
            
        except APIKey.DoesNotExist:
            logger.error("No User found with the access key.")
            raise exceptions.AuthenticationFailed("No User found with the access key.")
        except ValueError:
            logger.error("Badly formed hexadecimal UUID string.")
            raise exceptions.ValidationError("Badly formed hexadecimal UUID string.")
