from utils import get_root_path, join_path
import extract
import extract.parl_json as parl_json
import transform

# Ad-hoc script to get parliament files in the old format
# Old format is from 2012-08-13 and before
# From 2012-09-10 onwards, the JSON file format is different (V2)

root_path = get_root_path()
seed_dates_path = join_path(join_path(root_path, "seeds"), "dates.csv")

date_df = extract.get_dates_file(seed_dates_path)

date_list = list(date_df[date_df["Sitting_Date"] <= "2012-08-13"]["Sitting_Date"])


def get_json_html(date_list):
    for date in date_list:
        # Get JSON and Store JSON

        url = parl_json.parliament_url(parl_json.date_yyyymmdd_to_ddmmyyyy(date))

        response = parl_json.get_json(url)

        filepath = join_path(
            join_path(get_root_path(), "resource-archive-json"), f"{date}.json"
        )
        parl_json.save_json(response.json(), filepath)

        # Get HTML and Store HTML

        html = transform.get_json_archive(date, "htmlFullContent")

        filepath = join_path(
            join_path(get_root_path(), "resource-archive-html"), f"{date}.html"
        )

        with open(filepath, "w") as html_file:
            html_file.write(html)

    return 0


get_json_html(date_list)
