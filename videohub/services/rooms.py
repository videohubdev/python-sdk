class RoomService:

    def __init__(self, http):
        self.http = http

    async def create(self, **payload):

        if "room_name" not in payload:
            raise ValueError("room_name is required")

        payload.setdefault("mode", "df_video_party")
        payload.setdefault("max_participants", 5)

        return await self.http.post(
            "/client/create/rooms",
            payload,
            auth_required=True
    )

    async def host_token(self, room_name: str):

        return await self.http.post(
            "/client/rooms/token/host",
            {"room_name": room_name},
            auth_required=True
        )
        

    async def guest_token(self, room_name: str, app_id: str):

        return await self.http.post(
            "/rooms/token/guest",
            {"room_name": room_name, "app_id": app_id},
            auth_required=False
        )