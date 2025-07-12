import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class DebugLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log DEBUG status on each request
        logger.info(f"DEBUG mode is {'ENABLED' if settings.DEBUG else 'DISABLED'} - Request: {request.path}")
        
        response = self.get_response(request)
        return response 