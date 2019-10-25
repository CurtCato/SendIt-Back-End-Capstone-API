from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from SendItApp.models import *


class GymTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for gym/climbing_type join table

    Arguments:
        serializers
    """
    class Meta:
        model = GymType
        url = serializers.HyperlinkedIdentityField(
            view_name='gymtype',
            lookup_field='id'
        )
        fields = ('id', 'gym', 'climbing_type')
        depth = 2


class GymTypes(ViewSet):
    """Gym Types for Bangazon"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized gymtype instance
        """
        new_gymtype = GymType()
        new_gymtype.gym = Gym.objects.get(pk=request.data["gym_id"])
        new_gymtype.climbing_type = ClimbingType.objects.get(pk=request.data["climbing_type_id"])

        new_gymtype.save()

        serializer = GymTypeSerializer(new_gymtype, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single gymtype relationship

        Returns:
            Response -- JSON serialized gymtype instance
        """
        try:
            gymtype = GymType.objects.get(pk=pk)
            serializer = GymTypeSerializer(gymtype, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single order/product relationship

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            gymtype = GymType.objects.get(pk=pk)
            gymtype.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except GymType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests gym types resource

        Returns:
            Response -- JSON serialized list gym types
        """
        items = GymType.objects.all()

        serializer = GymTypeSerializer(
            items, many=True, context={'request': request})
        return Response(serializer.data)