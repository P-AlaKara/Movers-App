from django.urls import path
from .views import (
    MovingRequestListCreateView,
    MovingRequestDetailView,
    CancelRequestView,
    AvailableJobsView,
    PlaceBidView,
    AcceptBidView,
    CancelBidView,
    MyJobsView,
    StartJobView,
    CompleteJobView,
)

urlpatterns = [
    # Customer: moving requests
    path('requests/', MovingRequestListCreateView.as_view(), name='request-list-create'),
    path('requests/<int:request_id>/', MovingRequestDetailView.as_view(), name='request-detail'),
    path('requests/<int:request_id>/cancel/', CancelRequestView.as_view(), name='cancel-request'),

    # Mover: available jobs and bidding
    path('available/', AvailableJobsView.as_view(), name='available-jobs'),
    path('requests/<int:request_id>/bid/', PlaceBidView.as_view(), name='place-bid'),
    path('bids/<int:bid_id>/accept/', AcceptBidView.as_view(), name='accept-bid'),
    path('bids/<int:bid_id>/cancel/', CancelBidView.as_view(), name='cancel-bid'),

    # Mover: job lifecycle
    path('my/', MyJobsView.as_view(), name='my-jobs'),
    path('requests/<int:request_id>/start/', StartJobView.as_view(), name='start-job'),
    path('requests/<int:request_id>/complete/', CompleteJobView.as_view(), name='complete-job'),
]