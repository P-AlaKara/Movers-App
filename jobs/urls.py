from django.urls import path
from .views import (
    create_request_view,
    request_list,
    request_detail,
    available_jobs,
    accept_job,
    my_jobs,
    accept_mover
)

urlpatterns = [
    path("requests/create/", create_request_view, name="create_request"),
    path('requests/', request_list, name='request_list'),
    path('requests/<int:request_id>/', request_detail, name='request_detail'),
    path('jobs/', available_jobs, name='available_jobs'),
    path('jobs/<int:request_id>/accept/', accept_job, name='accept_job'),
    path('jobs/my-jobs/', my_jobs, name='my_jobs'),
    path('requests/<int:request_id>/accept-mover/', accept_mover, name='accept_mover'),
]