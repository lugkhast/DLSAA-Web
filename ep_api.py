
import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from models import *


dlsaa_api = endpoints.api(name='dlsaa-api', version='v1')
package = 'dlsaa_endpoints'


@dlsaa_api.api_class(resource_name='businesses')
class PartnerBusinessAPI(remote.Service):

    @endpoints.method(path='get-all')
    def get_all(self, request):
        