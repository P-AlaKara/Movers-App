from rest_framework import serializers
from .models import MovingRequest, Bid
from profiles.serializers import PublicMoverSerializer

class BidSerializer(serializers.ModelSerializer):
    mover = PublicMoverSerializer(source='mover.moverprofile', read_only=True)

    class Meta:
        model = Bid
        fields = ['id', 'mover', 'price', 'message', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']


class MovingRequestSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(source='customer.username', read_only=True)
    bids = BidSerializer(many=True, read_only=True)

    class Meta:
        model = MovingRequest
        fields = [
            'id', 'customer_username', 'pickup_location', 'dropoff_location',
            'moving_date', 'item_description', 'budget', 'status', 'created_at', 'bids'
        ]
        read_only_fields = ['status', 'created_at']


class MovingRequestListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views, it does not include bids"""
    customer_username = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = MovingRequest
        fields = [
            'id', 'customer_username', 'pickup_location', 'dropoff_location',
            'moving_date', 'budget', 'status', 'created_at'
        ]