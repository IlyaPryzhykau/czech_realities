"""
This module defines a custom authentication backend for the
sqladmin interface using basic credentials.
"""

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.core.config import settings


class BasicAuthBackend(AuthenticationBackend):
    """
    A basic authentication backend for the SQLAdmin panel.

    Attributes:
        secret_key (str): The secret key used as an additional
            security check (if desired).
    """

    async def login(self, request: Request) -> bool:
        """
        Handle the login form submission from the admin panel.

        Args:
            request (Request): The incoming request containing form data.

        Returns:
            bool: True if authentication succeeded, False otherwise.
        """
        form = await request.form()
        username = form.get('username')
        password = form.get('password')
        if (
            username == settings.first_superuser_email
            and password == settings.first_superuser_password
        ):
            request.session.update({'token': 'admin'})
            return True
        return False

    async def logout(self, request: Request) -> RedirectResponse:
        """
        Clear the admin session and redirect to the admin index page.

        Args:
            request (Request): The incoming request.

        Returns:
            RedirectResponse: A response redirecting to '/admin'.
        """
        request.session.clear()
        return RedirectResponse(url='/admin')

    async def authenticate(self, request: Request) -> bool:
        """
        Check if the user is already authenticated based on session data.

        Args:
            request (Request): The incoming request.

        Returns:
            bool: True if 'token' in session is 'admin', otherwise False.
        """
        return request.session.get('token') == 'admin'
