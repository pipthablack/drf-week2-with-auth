
from django.http import Http404
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework import viewsets
from Api.permissions import IsAdminOrReadOnly,IsReviewUserOrReadOnly
from rest_framework import generics
from .models import * 
from .serializers import * 

# Create your views here.


@api_view(["GET"])
def homepage(request):
    """
    This function handles the homepage request.

    Parameters:
    request (Request): The incoming request object.

    Returns:
    Response: A JSON response with a "message" key set to "Hello, world!".
    """
    return Response({"message": "Hello, world!"})



class WatchListAPIView(APIView):
    """
    This class-based view handles CRUD operations for WatchList objects.
    """

    def get(self, request):
        """
        This method handles GET requests to retrieve all WatchList objects.

        Parameters:
        request (Request): The incoming request object.

        Returns:
        Response: A JSON response containing serialized WatchList objects.
        """
        watchlists = WatchList.objects.all()
        serializer = WatchListSerializer(watchlists, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        This method handles POST requests to create a new WatchList object.

        Parameters:
        request (Request): The incoming request object containing the serialized data.

        Returns:
        Response: A JSON response containing the serialized WatchList object if successful,
        or a JSON response with errors if the data is invalid.
        """
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class WatchListDetailView(APIView):
    """
    This class-based view handles CRUD operations for a specific WatchList object.
    """

    def get_object(self, pk):
        """
        This method retrieves a WatchList object by its primary key.

        Parameters:
        pk (int): The primary key of the WatchList object.

        Returns:
        WatchList: The WatchList object if found, or raises a 404 exception if not found.
        """
        try:
            return WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        This method handles GET requests to retrieve a specific WatchList object.

        Parameters:
        request (Request): The incoming request object.
        pk (int): The primary key of the WatchList object.

        Returns:
        Response: A JSON response containing the serialized WatchList object.
        """
        watchlist = self.get_object(pk)
        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        This method handles PUT requests to update a specific WatchList object.

        Parameters:
        request (Request): The incoming request object containing the serialized data.
        pk (int): The primary key of the WatchList object.

        Returns:
        Response: A JSON response containing the serialized WatchList object if successful,
        or a JSON response with errors if the data is invalid.
        """
        watchlist = self.get_object(pk)
        serializer = WatchListSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StreamPlatformAPIView(APIView):
    """
    This class-based view handles CRUD operations for StreamPlatform objects.
    """

    def get(self, request):
        """
        This method handles GET requests to retrieve all StreamPlatform objects.

        Parameters:
        request (Request): The incoming request object.

        Returns:
        Response: A JSON response containing serialized StreamPlatform objects.
        """
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        This method handles POST requests to create a new StreamPlatform object.

        Parameters:
        request (Request): The incoming request object containing the serialized data.

        Returns:
        Response: A JSON response containing the serialized StreamPlatform object if successful,
        or a 404 response if the data is invalid.
        """
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



class StreamPlatformDetailView(APIView):
    """
    This class-based view handles CRUD operations for a specific StreamPlatform object.
    """

    def get(self, request, pk):
        """
        This method handles GET requests to retrieve a specific StreamPlatform object.

        Parameters:
        request (Request): The incoming request object.
        pk (int): The primary key of the StreamPlatform object.

        Returns:
        Response: A JSON response containing the serialized StreamPlatform object.
        """
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        This method handles PUT requests to update a specific StreamPlatform object.

        Parameters:
        request (Request): The incoming request object containing the serialized data.
        pk (int): The primary key of the StreamPlatform object.

        Returns:
        Response: A JSON response containing the serialized StreamPlatform object if successful,
        or a JSON response with errors if the data is invalid.
        """
        platform = self.get_object(pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        This method handles DELETE requests to delete a specific StreamPlatform object.

        Parameters:
        request (Request): The incoming request object.
        pk (int): The primary key of the StreamPlatform object.

        Returns:
        Response: A 204 No Content response if the deletion is successful.
        """
        platform = self.get_object(pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ReviewList(generics.ListAPIView):
    """
    This class-based view handles listing Review objects for a specific WatchList object.
    """
    serializer_class = ReviewSerializer
    # permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """
        This method retrieves the Review objects for a specific WatchList object.

        Parameters:
        None

        Returns:
        QuerySet: A QuerySet containing the Review objects for the specified WatchList object.
        """
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

    # def get(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)



class ReviewCreate(generics.CreateAPIView):
    """
    This class-based view handles creating a new Review object for a specific WatchList object.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This method retrieves all Review objects.

        Parameters:
        None

        Returns:
        QuerySet: A QuerySet containing all Review objects.
        """
        return Review.objects.all()

    def perform_create(self, serializer):
        """
        This method handles the creation of a new Review object.

        Parameters:
        serializer (ReviewSerializer): The serializer containing the validated data.

        Returns:
        None
        """
        watchlist = WatchList.objects.get(pk=self.kwargs['pk'])
        review_user = self.request.user
        # Use `filter()` instead of `all()` to filter the queryset
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You already have a review for this watchlist item.")
        
        # Update the watchlist's average rating
        if watchlist.number_rating == 0:
           watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating * watchlist.number_rating + serializer.validated_data['rating']) / (watchlist.number_rating + 1)
        
        watchlist.number_rating += 1
        watchlist.save()

        # Save the review with the associated watchlist and user
        serializer.save(watchlist=watchlist, review_user=review_user)



class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    This class-based view handles CRUD operations for a specific Review object.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrReadOnly]



class StreamPlatformVS(viewsets.ModelViewSet):
    """
    This class-based view handles CRUD operations for StreamPlatform objects using Django REST framework's ModelViewSet.
    """
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer