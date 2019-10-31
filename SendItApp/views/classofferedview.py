from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from SendItApp.models import ClassOffered, Gym


class ClassOfferedSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for ClassesOffered
    Author: Curt Cato

    Arguments:
        serializers
    """
    class Meta:
        model = ClassOffered
        url = serializers.HyperlinkedIdentityField(
            view_name='classoffered',
            lookup_field='id'
        )
        fields = ('id', 'url', 'class_name', 'description', 'days_offered', 'time_offered', 'gym', 'gym_id')
        depth = 2


class ClassesOffered(ViewSet):
    """Classes offered for SendIt """

    def create(self, request):
        """Handle POST operations

        Author: Curt Cato
        Purpose: Allow the user to create a class offered via communicating with the SendIt DB
        Method: POST

        Returns:
            Response -- JSON serialized order instance
        """

        new_class = ClassOffered()
        new_class.gym = Gym.objects.get(pk=request.data['gym_id'])
        new_class.class_name = request.data["class_name"]
        new_class.description = request.data["description"]
        new_class.days_offered = request.data["days_offered"]
        new_class.time_offered = request.data["time_offered"]
        # new_class is ready to save now
        new_class.save()
        # Convert the class to json and send it back to the client
        serializer = ClassOfferedSerializer(new_class, context={'request': request})
        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single class

        Author: Curt Cato
        Purpose: Allow a user to communicate with the SendIt database to retrieve one class
        Method:  GET

        Returns:
            Response -- JSON serialized class instance
        """
        try:
            class_offered = ClassOffered.objects.get(pk=pk)
            serializer = ClassOfferedSerializer(class_offered, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a class offered

        Author: Curt Cato
        Purpose: Allow a user to update an class via the SendIt DB
        Method: PUT

        Returns:
            Response -- Empty body with 204 status code
        """
        updated_class = ClassOffered.objects.get(pk=pk)
        updated_class.class_name = request.data["class_name"]
        updated_class.description = request.data["description"]
        updated_class.days_offered = request.data["days_offered"]
        updated_class.time_offered = request.data["time_offered"]

        updated_class.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a class are

        Author: Curt Cato
        Purpose: Allow a user to delete an class from the DB
        Method: DELETE

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            class_offered = ClassOffered.objects.get(pk=pk)
            class_offered.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ClassOffered.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to classes offered resource

        Author: Curt Cato
        Purpose: Allow a user to list all of the classes from the SendIt DB

        Returns:
            Response -- JSON serialized list of orders
        """
        classes_offered = ClassOffered.objects.all()

        gym = self.request.query_params.get('gym_id', None)

        if gym is not None:
            classes_offered = classes_offered.filter(gym_id=gym)

        serializer = ClassOfferedSerializer(
            classes_offered, many=True, context={'request': request}
        )
        return Response(serializer.data)