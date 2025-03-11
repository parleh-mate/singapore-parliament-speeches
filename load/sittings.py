import pandas as pd
import transform.sittings as sittings


def dataframe(metadata):
    sitting_df = pd.DataFrame(
        {
            "date": [sittings.date_str(metadata)],
            "datetime": [sittings.datetime_str(metadata)],
            "parliament": [metadata["parlimentNO"]],
            "session": [metadata["sessionNO"]],
            "volume": [metadata["volumeNO"]],
            "sittings": [metadata["sittingNO"]],
        }
    )

    return sitting_df
