import os

class AttachmentsAPI:

    MAX_FILE_SIZE = 1024 * 1024 * 1024

    def __init__(self, http):
        self.http = http

    async def upload(
        self,
        token: str,
        room_id: str,
        file_name: str,
        file_stream,
        mime_type: str = "application/octet-stream"
    ):

        file_stream.seek(0, os.SEEK_END)
        file_size = file_stream.tell()
        file_stream.seek(0)

        if file_size > self.MAX_FILE_SIZE:

            return {
                "status": False,
                "error": "Maximum file size is 1024MB"
            }
            

        files = {
            "file": (
                file_name,
                file_stream,
                mime_type
            )
        }

        data = {
            "room_id": room_id
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        res = await self.http.upload(
            endpoint="/attachments/upload",
            files=files,
            data=data,
            headers=headers
        )

        return res.get("data", res)
    

    async def download(
        self,
        attachment_id: str,
        save_path: str,
        token: str | None = None
    ):

        headers = {}

        if token:
            headers["Authorization"] = f"Bearer {token}"

        client = self.http._get_client()

        response = await client.get(
            f"/attachments/{attachment_id}/download",
            headers=headers,
            follow_redirects=True
        )

        response.raise_for_status()

        final_url = str(response.url)

        filename = (
            final_url
            .split("/")[-1]
            .split("?")[0]
        )

        full_path = os.path.join(
            save_path,
            filename
        )

        os.makedirs(
            os.path.dirname(full_path),
            exist_ok=True
        )

        with open(full_path, "wb") as f:
            f.write(response.content)

        return {
            "success": True,
            "path": full_path,
            "filename": filename
        }