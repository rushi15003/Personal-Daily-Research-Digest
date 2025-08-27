# src/agents/drive_upload.py
import os
from typing import Optional
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

load_dotenv()


SCOPES = ["https://www.googleapis.com/auth/drive.file"]


class DriveUploadAgent:
    """Uploads generated reports to a Google Drive folder.

    Requires either a user OAuth flow (credentials.json + token.json) or a service account.
    This implementation uses the user OAuth flow for simplicity (Drive File scope).
    """

    def __init__(self, credentials_path: str = "credentials.json", token_path: str = "token.json"):
        self.credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", credentials_path)
        self.token_path = os.getenv("GOOGLE_TOKEN_PATH", token_path)

    def _get_service(self):
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Google OAuth client secrets not found at {self.credentials_path}."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())
        return build("drive", "v3", credentials=creds)

    def upload_report(self, file_path: str, drive_folder_id: Optional[str] = None) -> Optional[str]:
        if not file_path or not os.path.exists(file_path):
            print(f"❌ Report file not found: {file_path}")
            return None
        service = self._get_service()
        file_metadata = {"name": os.path.basename(file_path)}
        if drive_folder_id:
            file_metadata["parents"] = [drive_folder_id]
        media = MediaFileUpload(file_path, mimetype="application/pdf")
        file = service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()
        file_id = file.get("id")
        web_view_link = file.get("webViewLink")
        print(f"✅ Uploaded to Drive. File ID: {file_id}, Link: {web_view_link}")
        return file_id


