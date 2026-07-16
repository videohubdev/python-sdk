class AdminService:

    def __init__(self, http):
        self.http = http

    async def kick(self, room: str, identity: str):

        return await self.http.post(
            "/client/va/kick",
            {
                "room_name": room,
                "identity": identity
            },
            auth_required=True
        )
        
        

    async def mute(self, room: str, identity: str):

        return await self.http.post(
            "/client/video-hub/mute",
            {
                "room_name": room,
                "identity": identity
            },
            auth_required=True
        )
        
        
    async def room_cleaner(self, room: str):
        
        return await self.http.post(
            "/client/video-hub/end",
            {
                "room_name": room,
            },
            auth_required=True
        )