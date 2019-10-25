from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from SendItApp.models import *
from django.contrib.auth.models import User


class GymSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for gyms

        Arguments:
        serializers.HyperlinkedModelSerializer
    """
    # This meta defines the field and the model that is being used
    class Meta:
        model = Gym
        url = serializers.HyperlinkedIdentityField(
        view_name='gym',
        lookup_field='id'
        )

        fields = ('id', 'gym_name', 'street_address', 'city',
          'state', 'longitude', 'latitude', 'climber', 'gym_size', 'wall_height' 'url')
        depth = 1


class Gyms(ViewSet):
    """Handle POST operations
        Returns:
            Response -- JSON serialized gym instance
        """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def create(self, request):
        new_gym = Gym()
        new_gym.climber = Climber.objects.get(user=request.auth.user)
        new_gym.gym_name = request.data["gym_name"]
        new_gym.street_address = request.data["street_address"]
        new_gym.state = request.data["state"]
        new_gym.city = request.data["city"]
        new_gym.longitude = request.data["longitude"]
        new_gym.latitude = request.data["latitude"]
        new_gym.gym_size = request.data["gym_size"]
        new_gym.wall_height = request.data["wall_height"]
        new_gym.save()
        serializer = GymSerializer(new_gym, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single gym
        Returns:
            Response -- JSON serialized gym instance
        """
        try:
            gym = Gym.objects.get(pk=pk)
            serializer = GymSerializer(gym, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a gym
        Returns:
            Response -- Empty body with 204 status code
        """
        updated_gym = Gym.objects.get(pk=pk)
        updated_gym.gym_name = request.data["gym_name"]
        updated_gym.street_address = request.data["street_address"]
        updated_gym.state = request.data["state"]
        updated_gym.city = request.data["city"]
        updated_gym.longitude = request.data["longitude"]
        updated_gym.latitude = request.data["latitude"]
        updated_gym.gym_size = request.data["gym_size"]
        updated_gym.wall_height = request.data["wall_height"]
        updated_gym.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single gym
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            gym= Gym.objects.get(pk=pk)
            gym.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Gym.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to gyms resource
        Returns:
            Response -- JSON serialized list of gyms
        """
        gyms = Gym.objects.all()  # This is my query to the database

        serializer = GymSerializer(
            gyms, many=True, context={'request': request})
        return Response(serializer.data)