from googleapiclient.discovery import build
from google.oauth2 import service_account
from Google import Create_Service

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'TienHoa_Acc1.json'
PARENT_FOLDER_ID = "1gIcSZozWAYfAKtnt5hpon3HRs73wI_KI"

# service = Create_Service(SERVICE_ACCOUNT_FILE,"drive","v3",SCOPES)

# def authenticate():
#     creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#     return creds

# def upload_photo(file_path):
#     creds = authenticate()
#     service = build('drive', 'v3', credentials=creds)

#     file_metadata = {
#         'name' : "Test",
#         'parents' : [PARENT_FOLDER_ID]
#     }

#     file = service.files().create(
#         body=file_metadata,
#         media_body=file_path
#     ).execute()
    
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly","https://www.googleapis.com/auth/drive"]


def upload_file(file_path):
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None

  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "TienHoa_Acc1.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("drive", "v3", credentials=creds)

    file_metadata = {
            'name' : "Test",
            'parents' : [PARENT_FOLDER_ID]
        }

    file = service.files().create(
            body=file_metadata,
            media_body="path"
        ).execute()
  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  upload_file("test.pdf")

# upload_photo("test.pdf")