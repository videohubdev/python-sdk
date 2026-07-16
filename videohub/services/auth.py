class AuthService:

    def __init__(self, http):
        self.http = http

    async def init(self, login: str, password: str):

        return await self.http.post(
            "/client/auth/session",
            {
                "login": login,
                "password": password
            },
            auth_required=True
        )