from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from SendItApp.models import *
from django.contrib.auth.models import User
from key import GoogleToken
import googlemaps

class ClimbingSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for gyms

        Arguments:
        serializers.HyperlinkedModelSerializer
    """
    # This meta defines the field and the model that is being used
    class Meta:
        model = ClimbingType
        url = serializers.HyperlinkedIdentityField(
        view_name='climbingType',
        lookup_field='id'
        )

        fields = ('id', 'type_name')

class GymTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for gyms

        Arguments:
        serializers.HyperlinkedModelSerializer
    """
    # This meta defines the field and the model that is being used
    climbing_type=ClimbingSerializer(many=False)
    class Meta:
        model = GymType
        url = serializers.HyperlinkedIdentityField(
        view_name='gymType',
        lookup_field='id'
        )

        fields = ('id', 'climbing_type')

class GymSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for gyms

        Arguments:
        serializers.HyperlinkedModelSerializer
    """
    # This meta defines the field and the model that is being used
    matching_types=GymTypeSerializer(many=True)
    class Meta:
        model = Gym
        url = serializers.HyperlinkedIdentityField(
        view_name='gym',
        lookup_field='id'
        )

        fields = ('id', 'matching_types', 'climber_id', 'gym_name', 'street_address', 'longitude', 'latitude', 'climber', 'gym_size', 'wall_height', 'url')
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
        gmaps = googlemaps.Client(key=GoogleToken)
        geocode_result = gmaps.geocode(request.data['street_address'])[0]
        new_gym.latitude = geocode_result['geometry']['location']['lat']
        new_gym.longitude = geocode_result['geometry']['location']['lng']
        new_gym.gym_size = request.data["gym_size"]
        new_gym.wall_height = request.data["wall_height"]
        new_gym.save()


        selectedTypes = request.data["selectedCLimbingTypes"]
        for climbTypeId in selectedTypes:
            climbType = GymType()
            climbType.gym = new_gym
            climbType.climbing_type = ClimbingType.objects.get(pk=int(climbTypeId))
            climbType.save()


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
        gmaps = googlemaps.Client(key=GoogleToken)
        geocode_result = gmaps.geocode(request.data['street_address'])[0]
        updated_gym.latitude = geocode_result['geometry']['location']['lat']
        updated_gym.longitude = geocode_result['geometry']['location']['lng']
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
        climber = Climber.objects.get(user=request.auth.user)

        serializer = GymSerializer(
            gyms, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def usergyms(self, request):
        climber = Climber.objects.get(user=request.auth.user)
        gyms = Gym.objects.all()
        gyms= gyms.filter(climber=climber)
        serializer = GymSerializer(
            gyms, many=True, context={'request': request})
        return Response(serializer.data)