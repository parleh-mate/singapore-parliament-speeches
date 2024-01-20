import pandas as pd
import transform.sittings as sittings

def dataframe(metadata):

    sitting_df = pd.DataFrame(
        {
            "Sitting_CID": [sittings.cid(metadata)],
            "Sitting_Date": [sittings.datetime_str(metadata)],
            "Parliament Session Str": [metadata["partSessionStr"]],
            "Parliament_Number": [metadata["parlimentNO"]],
            "Session_Number": [metadata["sessionNO"]],
            "Volume_Number": [metadata["volumeNO"]],
            "Sitting_Number": [metadata["sittingNO"]],
        }
    )

    return sitting_df
