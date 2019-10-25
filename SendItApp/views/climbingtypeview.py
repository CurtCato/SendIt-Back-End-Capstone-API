from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from SendItApp.models import *
from SendItApp.views import *

class ClimbingTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for climbing types

    Arguments:
        serializers
    """

    class Meta:
        model = ClimbingType
        url = serializers.HyperlinkedIdentityField(
            view_name='climbingtype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'type_name')
        depth = 2


class ClimbingTypes(ViewSet):
    """Product types for SendItn"""

    permission_classes = (IsAuthenticatedOrReadOnly,)
    def create(self, request):

        """Handle POST operations

        Returns:
            Response -- JSON serialized ProductType instance
        """

        new_climbing_type = ClimbingType()
        new_climbing_type.type_name = request.data["type_name"]
        new_climbing_type.save()

        serializer = ClimbingTypeSerializer(new_climbing_type, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single climbing type

        Returns:
            Response -- JSON serialized climbingType instance
        """
        try:
            climbing_type = ClimbingType.objects.get(pk=pk)
            serializer = ClimbingTypeSerializer(climbing_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a climbing type

        Returns:
            Response -- Empty body with 204 status code
        """
        climbing_type = ClimbingType.objects.get(pk=pk)
        climbing_type.type_name = request.data["type_name"]
        climbing_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single climbing type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            climbing_type = ClimbingType.objects.get(pk=pk)
            climbing_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ClimbingType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to climbing types resource

        Returns:
            Response -- JSON serialized list of climbing types
        """
        types = ClimbingType.objects.all()

        serializer = ClimbingTypeSerializer(
            types, many=True, context={'request': request})
        return Response(serializer.data)