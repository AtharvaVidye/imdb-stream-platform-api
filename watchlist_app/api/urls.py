from django.urls import include, path
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import StreamPlatformVS , ReviewCreate, ReviewDetail, ReviewList, UserReview, WatchList, WatchListAV, WatchDetailAV, StreamPlatformAV , StreamPlatformDetailAV

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='Watch_list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='Watchlist_details'),
    path('list2/', WatchList.as_view(), name='watch-list'),
    path('' , include(router.urls)) ,
    # path('stream/', StreamPlatformAV.as_view(), name='Stream'),
    # path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='StreamPlatform_details'),
    # path('review/<int:pk>/', ReviewDetail.as_view(), name='review_detail'),
    # path('review/', ReviewList.as_view(), name='review_list'),
    path('stream/<int:pk>/review-create/', ReviewCreate.as_view(), name='review_create'),
    path('stream/<int:pk>/review/', ReviewList.as_view(), name='review_list'),
    path('stream/review/<str:username>/', UserReview.as_view(), name='user-review_detail'),
  
]
