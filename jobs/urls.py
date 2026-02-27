from django.urls import path
from .views import (
    create_request_view,
    request_list,
    request_detail,
    available_jobs,
    my_jobs,
    complete_job, 
    cancel_request,
    place_bid,
    accept_bid, 
    cancel_bid,
    start_job,
)

urlpatterns = [
    # Customer request routes
    path("requests/create/", create_request_view, name="create_request"),
    path("requests/", request_list, name="request_list"),
    path("requests/<int:request_id>/", request_detail, name="request_detail"),
    path("requests/<int:request_id>/cancel/", cancel_request, name="cancel_request"),

    # Bidding system
    path("jobs/available/", available_jobs, name="available_jobs"),
    path("jobs/<int:request_id>/bid/", place_bid, name="place_bid"),
    path("bids/<int:bid_id>/accept/", accept_bid, name="accept_bid"),
    path("bids/<int:bid_id>/cancel/", cancel_bid, name="cancel_bid"),

    # Mover job lifecycle
    path("jobs/my/", my_jobs, name="my_jobs"),
    path("jobs/<int:request_id>/start/", start_job, name="start_job"),
    path("jobs/<int:request_id>/complete/", complete_job, name="complete_job"),
]