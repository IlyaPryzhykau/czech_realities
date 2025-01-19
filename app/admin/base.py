from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.core.config import settings


class BasicAuthBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
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
        request.session.clear()
        return RedirectResponse(url='/admin')

    async def authenticate(self, request: Request) -> bool:
        return request.session.get('token') == 'admin'
