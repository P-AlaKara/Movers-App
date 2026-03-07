from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from jobs.models import MovingRequest, Bid
from jobs.serializers import MovingRequestListSerializer
from notifications.models import Notification


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role = request.user.profile.role
        status_filter = request.query_params.get('status')
        unread_notifications = request.user.notifications.filter(is_read=False).count()

        if role == 'customer':
            return self._customer_dashboard(request, status_filter, unread_notifications)
        elif role == 'mover':
            return self._mover_dashboard(request, status_filter, unread_notifications)

    def _customer_dashboard(self, request, status_filter, unread_notifications):
        requests = MovingRequest.objects.filter(customer=request.user)

        stats = {
            'total': requests.count(),
            'open': requests.filter(status='open').count(),
            'accepted': requests.filter(status='accepted').count(),
            'completed': requests.filter(status='completed').count(),
            'cancelled': requests.filter(status='cancelled').count(),
        }

        if status_filter:
            requests = requests.filter(status=status_filter)

        serializer = MovingRequestListSerializer(
            requests.order_by('-created_at'),
            many=True
        )

        return Response({
            'role': 'customer',
            'stats': stats,
            'requests': serializer.data,
            'unread_notifications': unread_notifications,
        })

    def _mover_dashboard(self, request, status_filter, unread_notifications):
        bids = Bid.objects.filter(mover=request.user).select_related('moving_request')
        jobs = MovingRequest.objects.filter(
            bids__mover=request.user,
            bids__status='accepted'
        ).distinct()

        job_stats = {
            'total': jobs.count(),
            'accepted': jobs.filter(status='accepted').count(),
            'in_progress': jobs.filter(status='in_progress').count(),
            'completed': jobs.filter(status='completed').count(),
            'cancelled': jobs.filter(status='cancelled').count(),
        }

        bid_stats = {
            'total': bids.count(),
            'pending': bids.filter(status='pending').count(),
            'accepted': bids.filter(status='accepted').count(),
            'rejected': bids.filter(status='rejected').count(),
            'cancelled': bids.filter(status='cancelled').count(),
        }

        if status_filter:
            jobs = jobs.filter(status=status_filter)

        serializer = MovingRequestListSerializer(
            jobs.order_by('-moving_date'),
            many=True
        )

        return Response({
            'role': 'mover',
            'stats': {
                'job_stats': job_stats,
                'bid_stats': bid_stats,
            },
            'jobs': serializer.data,
            'unread_notifications': unread_notifications,
        })