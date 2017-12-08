from urllib import request as http
import json

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django.db.models import F

from .models import Zipcode
from .serializers import ZipcodeSerializer
from .constants import GOOGLE_MAPS_URL


def extract_zipcodes(data):
    address_components = []
    for result in data.get('results', []):
        for component in result['address_components']:
            if 'postal_code' in component['types'] and component['long_name'] not in address_components:
                address_components.append(component['long_name'])

    return address_components


class ZipcodeView(viewsets.ModelViewSet):
    queryset = Zipcode.objects.all().order_by('-query_count')
    serializer_class = ZipcodeSerializer

    @list_route()
    def search(self, request):
        params = request.query_params
        lat = params.get('lat')
        lng = params.get('lng')

        if not lng or not lat:
            return Response(status=401, data={'error': 'malformed query parameters'})
            # handle error here.

        url = "{google_url}&latlng={lat},{lng}".format(
            google_url=GOOGLE_MAPS_URL,
            lat=lat,
            lng=lng
        )
        # double check this. See if Django has it's own way....

        response = http.urlopen(url)
        google_data = response.read().decode('utf-8')
        data_payload = {}
        data = json.loads(google_data)
        status = data.get('status', 'UNKNOWN_ERROR')

        if status == 'OK':
            zipcodes = extract_zipcodes(data)
            for zip in self.get_queryset().filter(zipcode__in=zipcodes):
                zip.query_count = F('query_count') + 1
                zip.save()

            data_payload['data'] = zipcodes
            return Response(status=200, data=data_payload)

        if status == 'ZERO_RESULTS':
            data_payload['data'] = []
            return Response(status=200, data=data_payload)

        data_payload['error'] = data.get('error_message', '')
        return Response(status=response.status, data=data_payload)

    @list_route()
    def top(self, request):
        zipcodes = self.get_queryset().filter(query_count__gt=0)[:5]
        serializer = self.get_serializer(zipcodes, many=True)

        return Response(status=200, data=serializer.data)
