import requests
import pandas as pd
from google.cloud import bigquery
import pandas_gbq
import os


class ParliamentAPI:
    def __init__(self):
        self.base_url = "https://www.sgparliament.com/api/parliament/sittings"

    def download_data(self, sitting_date, page=1, per_page=20):
        url = self.base_url
        params = {"sitting_date": sitting_date, "page": page, "per_page": per_page}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None


class ParliamentData:
    def __init__(self, data):
        self.data = data

    def to_dataframe(self):
        # Define column names and data types
        columns = {
            "id": int,
            "title": str,
            "mp_name": str,
            "parliament_no": int,
            "session_no": int,
            "volume_no": int,
            "sitting_no": int,
            "sitting_date": str,  # converted to datetime
            "mp_role": str,
            "mp_constituency": str,
            "section_event_id": int,
            "question_content": str,
            "raw_speaker": str,
        }

        # Create DataFrame with specified columns and data types
        df = pd.DataFrame(self.data["data"], columns=columns.keys()).astype(columns)
        df["sitting_date"] = pd.to_datetime(df["sitting_date"])

        return df

    def to_bigquery(self, project_id, dataset_id, table_id):
        # Write DataFrame to BigQuery
        table_ref = f"{project_id}.{dataset_id}.{table_id}"

        pandas_gbq.to_gbq(
            dataframe=self.to_dataframe(),
            destination_table=table_ref,
            project_id=project_id,
            if_exists="append",
        )


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "token/gcp_token.json"
project_id = "singapore-parliament-speeches"

query = """
  select sitting_date from `singapore-parliament-speeches.sgparl_api.sitting_results` where sitting_date >= '2009-09-14'
  order by sitting_date
"""

sitting_dates_df = pandas_gbq.read_gbq(query, project_id)
sitting_dates = sitting_dates_df["sitting_date"].to_list()

total_pages = []
parliament_api = ParliamentAPI()

for sitting_date in sitting_dates:
    for page in range(1, 1000):
        data = parliament_api.download_data(
            sitting_date=sitting_date, page=page, per_page=50
        )

        if data["data"]:
            print(f"Uploading: Sitting Date: {sitting_date}, Page: {page}")
            parliament_data = ParliamentData(data)
            parliament_data.to_bigquery(
                project_id=project_id, dataset_id="sgparl_api", table_id="speeches"
            )
        else:
            print(f"End at: Sitting Date: {sitting_date}, Page: {page-1}")
            total_pages.append(page - 1)
            break
