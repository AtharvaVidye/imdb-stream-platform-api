from watchlist_app.api.serializers import ReviewSerializer, WatchlistSerializer, StreamPlatformSerializer
from watchlist_app.models import Review, Watchlist, StreamPlatform
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
# from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated
from watchlist_app.api.permissions import AdminOrReadOnly , ReviewUserOrReadOnly

from rest_framework.throttling import UserRateThrottle , AnonRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle , ReviewListThrottle

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # throttle_classes = [ReviewListThrottle , AnonRateThrottle]
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = get_object_or_404(Watchlist, pk=pk)

        user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=user)

        if review_queryset.exists():
            raise ValidationError('You have already reviewed this movie.')
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
            
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=user)



class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewListThrottle , AnonRateThrottle]
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)  # Changed 'Watchlist' to 'watchlist'

    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_classes = [UserRateThrottle , AnonRateThrottle]
    
    permission_classes = [ReviewUserOrReadOnly]

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [AdminOrReadOnly]
    


# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         stream_platform = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(stream_platform)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StreamPlatformAV(APIView):
    
    permission_classes = [AdminOrReadOnly]
    
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StreamPlatformDetailAV(APIView):
    
    permission_classes = [AdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(platform)
            return Response(serializer.data)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Stream Platform Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(platform, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Stream Platform Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            platform.delete()
            return Response({'Message': 'Stream Platform deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Stream Platform Not Found'}, status=status.HTTP_404_NOT_FOUND)


# class WatchList(generics.ListAPIView):
#     queryset = Watchlist.objects.all()
#     serializer_class = WatchlistSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['title', 'platform__name']
    

class WatchList(generics.ListAPIView):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'platform__name']
    
class WatchListAV(APIView):
    
    permission_classes = [AdminOrReadOnly]
    
    def get(self, request):
        watchlists = Watchlist.objects.all()
        serializer = WatchlistSerializer(watchlists, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchDetailAV(APIView):
    
    permission_classes = [AdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            watchlist = Watchlist.objects.get(pk=pk)
            serializer = WatchlistSerializer(watchlist)
            return Response(serializer.data)
        except Watchlist.DoesNotExist:
            return Response({'Error': 'Watchlist Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        try:
            watchlist = Watchlist.objects.get(pk=pk)
            serializer = WatchlistSerializer(watchlist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Watchlist.DoesNotExist:
            return Response({'Error': 'Watchlist Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            watchlist = Watchlist.objects.get(pk=pk)
            watchlist.delete()
            return Response({'Message': 'Watchlist deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Watchlist.DoesNotExist:
            return Response({'Error': 'Watchlist Not Found'}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['GET', 'POST'])
# def Watchlist_list(request):
    
#     if request.method == 'GET':
#         Watchlists = Watchlist.objects.all()
#         serializer = WatchlistSerializer(Watchlists , many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = WatchlistSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data , status=201)
#         return Response(serializer.errors , status=400)



# @api_view(['GET', 'PUT', 'DELETE'])
# def Watchlist_details(request , pk):
    
#     if request.method == 'GET':
#         try:
#             Watchlist = Watchlist.objects.get(pk=pk)
#             serializer = WatchlistSerializer(Watchlist)
#             return Response(serializer.data)
#         except:
#             return Response( {'Error' : 'Watchlist Not Found' } , status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         Watchlist = Watchlist.objects.get(pk=pk)
#         serializer = WatchlistSerializer(Watchlist , data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors , status=400)
    
#     if request.method == 'DELETE':
#         Watchlist = Watchlist.objects.get(pk=pk)
#         Watchlist.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
    

