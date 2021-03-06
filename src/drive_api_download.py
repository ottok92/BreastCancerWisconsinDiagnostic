import io
import os
import pickle
import sys, argparse
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def download_data(file_id, output):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    if not file_id:
        sys.exit(
            "\nMissing arguments. Correct usage:\npython drive_api_download.py --file_id <file_id> [--output output_name]\n"
        )
    elif not output:
        output = "./" + file_id

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("drive", "v3", credentials=creds)

    # Downloads file
    request = service.files().export_media(fileId=file_id, mimeType="text/csv")
    fp = open(output, "wb")
    downloader = MediaIoBaseDownload(fp, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk(num_retries=3)
        print("Download %d%%." % int(status.progress() * 100))
        
    fp.close()
    return done


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--file_id")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()

    download_data(args.file_id, args.output)
