from django.shortcuts import redirect
from django.urls import reverse

class SessionExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request): 
        
        if request.session.get_expiry_age() <= 0:
            # Session has expired, redirect to the desired view
            return redirect(reverse('logout'))  # Replace 'session_expired_view' with the actual name of the view function

        response = self.get_response(request)

        return response
