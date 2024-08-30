from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
class ClubApprovalMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.user.is_club() and not request.user.is_active:
            return Response({'erreur': 'Your account is not approved yet'}, status=403)  # Return a 403 Forbidden response
        return None