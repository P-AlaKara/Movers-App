from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'message': 'Welcome to the Songa API',
        'status': 'online',
        'endpoints': {
            'auth': {
                'register': '/accounts/register/',
                'login': '/accounts/login/',
                'token_refresh': '/accounts/token/refresh/',
            },
            'profiles': {
                'me': '/profiles/me/',
                'movers': '/profiles/movers/',
                'mover_detail': '/profiles/movers/<id>/',
            },
            'jobs': {
                'requests': '/jobs/requests/',
                'request_detail': '/jobs/requests/<id>/',
                'cancel_request': '/jobs/requests/<id>/cancel/',
                'available_jobs': '/jobs/available/',
                'place_bid': '/jobs/requests/<id>/bid/',
                'accept_bid': '/jobs/bids/<id>/accept/',
                'cancel_bid': '/jobs/bids/<id>/cancel/',
                'my_jobs': '/jobs/my/',
                'start_job': '/jobs/requests/<id>/start/',
                'complete_job': '/jobs/requests/<id>/complete/',
            },
            'dashboard': {
                'dashboard': '/dashboard/',
            },
            'notifications': {
                'list': '/notifications/',
                'mark_read': '/notifications/<id>/read/',
                'mark_all_read': '/notifications/read-all/',
            },
        }
    })