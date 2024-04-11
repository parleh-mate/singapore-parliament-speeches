import requests
import datetime
from googleapiclient.http import MediaFileUpload
import tempfile
import json

### Methods ###

def find_folder_id(service, folder_name):
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = response.get('files', [])
    if files:
        return files[0]['id']  # Assuming the first match is the correct one
    else:
        print(f"Could not find {folder_name}")
    return None


def date_yyyymmdd_to_ddmmyyyy(date_yyyymmdd):
    date_obj = datetime.datetime.strptime(date_yyyymmdd, "%Y-%m-%d")
    return date_obj.strftime("%d-%m-%Y")


def parliament_url(date_ddmmyyyy):
    return (
        f"https://sprs.parl.gov.sg/search/getHansardReport/?sittingDate={date_ddmmyyyy}"
    )


def get_json(url):
    print(f"Trying: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Success!")
    else:
        print(f"Reponse Code: {response.status_code}")

    return response


def upload_json(response_json, file, folder_id):

    # Upload the file
        file_metadata = {
            'name': file,
            'parents': [folder_id]
        }

        # Create a temporary file; gdrive has to upload from path and not saved object
        with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.json') as temp_file:
             json.dump(response_json, temp_file)
             temp_file_path = temp_file.name 

        media = MediaFileUpload(temp_file_path, mimetype='application/json')

        # automatically overwrites if exists

        uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        
        print(f"Uploaded {filename} with ID: {uploaded_file.get('id')}")
        
        return 0
