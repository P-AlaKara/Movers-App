from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import MovingRequest, Bid
from .serializers import MovingRequestSerializer, MovingRequestListSerializer, BidSerializer
from notifications.utils import create_notification
from .permissions import IsCustomer, IsMover


# Customer: Moving Requests 

class MovingRequestListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MovingRequestSerializer
        return MovingRequestListSerializer

    def get_queryset(self):
        return MovingRequest.objects.filter(
            customer=self.request.user
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user, status='open')


class MovingRequestDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    serializer_class = MovingRequestSerializer

    def get_object(self):
        return get_object_or_404(
            MovingRequest,
            id=self.kwargs['request_id'],
            customer=self.request.user
        )


class CancelRequestView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request, request_id):
        moving_request = get_object_or_404(
            MovingRequest,
            id=request_id,
            customer=request.user
        )

        if moving_request.status not in ['open', 'accepted']:
            return Response(
                {'error': 'Only open or accepted requests can be cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        moving_request.status = 'cancelled'
        moving_request.save()

        accepted_bid = moving_request.bids.filter(status='accepted').first()
        if accepted_bid:
            create_notification(
                user=accepted_bid.mover,
                message=f"The moving request #{moving_request.id} was cancelled.",
                link=f"/dashboard/"
            )

        return Response({'detail': 'Request cancelled.'})


# Mover: Available Jobs & Bidding
class AvailableJobsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsMover]
    serializer_class = MovingRequestListSerializer

    def get_queryset(self):
        mover_profile = self.request.user.moverprofile
        return MovingRequest.objects.filter(
            status='open',
            pickup_location__icontains=mover_profile.service_area
        ).order_by('moving_date')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        existing_bids = Bid.objects.filter(
            mover=request.user,
            moving_request__in=queryset
        ).values_list('moving_request_id', flat=True)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['already_bid'] = list(existing_bids)
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'jobs': serializer.data,
            'already_bid': list(existing_bids)
        })


class PlaceBidView(APIView):
    permission_classes = [IsAuthenticated, IsMover]

    def post(self, request, request_id):
        moving_request = get_object_or_404(MovingRequest, id=request_id, status='open')

        if Bid.objects.filter(moving_request=moving_request, mover=request.user).exists():
            return Response(
                {'error': 'You have already placed a bid on this request.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(moving_request=moving_request, mover=request.user)
            create_notification(
                user=moving_request.customer,
                message=f"New bid placed on your request #{moving_request.id}.",
                link=f"/jobs/requests/{moving_request.id}/"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelBidView(APIView):
    permission_classes = [IsAuthenticated, IsMover]

    def post(self, request, bid_id):
        bid = get_object_or_404(Bid, id=bid_id, mover=request.user)

        if bid.status != 'pending':
            return Response(
                {'error': 'Only pending bids can be cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        bid.status = 'cancelled'
        bid.save()
        return Response({'detail': 'Bid cancelled.'})


# Customer: Accept a Bid
class AcceptBidView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request, bid_id):
        bid = get_object_or_404(Bid, id=bid_id)

        if bid.moving_request.customer != request.user:
            return Response(
                {'error': 'You do not own this request.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if bid.moving_request.status != 'open':
            return Response(
                {'error': 'This request is no longer open.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        bid.status = 'accepted'
        bid.save()

        Bid.objects.filter(
            moving_request=bid.moving_request
        ).exclude(id=bid.id).update(status='rejected')

        bid.moving_request.status = 'accepted'
        bid.moving_request.save()

        create_notification(
            user=bid.mover,
            message=f"Your bid for request #{bid.moving_request.id} was accepted!",
            link=f"/dashboard/"
        )

        return Response({'detail': 'Bid accepted.'})


# Mover: Job Lifecycle

class MyJobsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsMover]
    serializer_class = MovingRequestListSerializer

    def get_queryset(self):
        return MovingRequest.objects.filter(
            bids__mover=self.request.user,
            bids__status='accepted',
            status__in=['accepted', 'in_progress', 'completed']
        ).distinct().order_by('-moving_date')


class StartJobView(APIView):
    permission_classes = [IsAuthenticated, IsMover]

    def post(self, request, request_id):
        job = get_object_or_404(
            MovingRequest,
            id=request_id,
            bids__mover=request.user,
            bids__status='accepted'
        )

        if job.status != 'accepted':
            return Response(
                {'error': 'Job must be in accepted state to start.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        job.status = 'in_progress'
        job.save()

        create_notification(
            user=job.customer,
            message=f"Your move #{job.id} has started.",
            link=f"/jobs/requests/{job.id}/"
        )

        return Response({'detail': 'Job started.'})


class CompleteJobView(APIView):
    permission_classes = [IsAuthenticated, IsMover]

    def post(self, request, request_id):
        job = get_object_or_404(
            MovingRequest,
            id=request_id,
            bids__mover=request.user,
            bids__status='accepted'
        )

        if job.status != 'in_progress':
            return Response(
                {'error': 'Job must be in progress to complete.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        job.status = 'completed'
        job.save()

        create_notification(
            user=job.customer,
            message=f"Your move #{job.id} has been completed.",
            link=f"/jobs/requests/{job.id}/"
        )

        return Response({'detail': 'Job completed.'})