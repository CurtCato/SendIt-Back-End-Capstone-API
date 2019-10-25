from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from SendItApp.models import Climber



class ClimberSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Climbers
    Arguments:
        serializers
    """

    class Meta:
        model = Climber
        url = serializers.HyperlinkedIdentityField(
            view_name='climber',
            lookup_field='id'
        )
        fields = ('id', 'url', 'user', 'user_id')
        depth = 2

class Climbers(ViewSet):

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Attraction instance
        """
        new_climber = Climber()

        user = Climber.objects.get(user=request.auth.user)
        new_climber.user = user
        new_climber.save()

        serializer = ClimberSerializer(new_climber, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a single payment type

        Returns:
            Response -- Empty body with 204 status code
        """
        update_climber = Climber.objects.get(pk=pk)

        user = User.objects.get(pk=request.data["user_id"])

        user.email = request.data["email"]
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]

        user.save()

        update_climber.user = user

        update_climber.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a climber are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            climber = Climber.objects.get(pk=pk)
            climber.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Climber.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single climber
        Returns:
            Response -- JSON serialized climber instance
        """
        try:
            climber = climber.objects.get(pk=pk)
            serializer = ClimberSerializer(climber, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        climbers = Climber.objects.all()

        serializer = ClimberSerializer(
            climbers, many=True, context={'request': request})
        return Response(serializer.data)