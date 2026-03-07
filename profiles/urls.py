from django.urls import path
from .views import MyProfileView, MoverListView, MoverDetailView

urlpatterns = [
    path('me/', MyProfileView.as_view(), name='my-profile'),
    path('movers/', MoverListView.as_view(), name='mover-list'),
    path('movers/<int:pk>/', MoverDetailView.as_view(), name='mover-detail'),
]