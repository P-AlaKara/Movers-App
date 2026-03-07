from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import MoverProfile
from .serializers import ProfileSerializer, MoverProfileSerializer

class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile_data = ProfileSerializer(request.user.profile).data

        if request.user.profile.role == 'mover':
            mover_profile = MoverProfile.objects.get(user=request.user)
            mover_data = MoverProfileSerializer(mover_profile).data
            return Response({**profile_data, 'mover_profile': mover_data})

        return Response(profile_data)

    def patch(self, request):
        profile = request.user.profile
        profile_serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if request.user.profile.role == 'mover':
            mover_profile = MoverProfile.objects.get(user=request.user)
            mover_serializer = MoverProfileSerializer(mover_profile, data=request.data.get('mover_profile', {}), partial=True)

            if profile_serializer.is_valid() and mover_serializer.is_valid():
                profile_serializer.save()
                mover_serializer.save()
                return Response({
                    **profile_serializer.data,
                    'mover_profile': mover_serializer.data
                })

            errors = {**profile_serializer.errors, **mover_serializer.errors}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data)

        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)