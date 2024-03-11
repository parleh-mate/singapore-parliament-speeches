import pandas as pd
import transform.topics as topics
import transform.speeches as speeches


def processing(date_yyyymmdd, topics_list):
    df = None

    orders = list(range(1, len(topics_list) + 1))
    topic_cids = [topics.topic_cid(date_yyyymmdd, order) for order in orders]

    for index, topic in enumerate(topics_list):
        topic_cid = topic_cids[index]
        temp_df = speeches.topic_dataframe(topic["content"], topic_cid, index)

        if df is None:
            df = temp_df
        else:
            df = pd.concat([df, temp_df], ignore_index=True)

    speech_orders = list(range(1, len(df) + 1))
    df["speech_order"] = speech_orders
    df["speech_id"] = df.apply(speeches.speech_cid, axis=1)

    result = df.apply(speeches.count_words_and_characters, axis=1)
    df = pd.concat([df, result[["num_words", "num_characters"]]], axis=1)

    return df


def dataframe(date_yyyymmdd, topics_list):
    df = processing(date_yyyymmdd, topics_list)

    speeches_df = pd.DataFrame(
        {
            "speech_id": df["speech_id"],
            "topic_id": df["Topic_CID"],
            "speech_order": df["speech_order"],
            "member_name_original": df["Original_MP_Name"],
            "member_name": df["MP_Name"],
            "text": df["Text"],
            "num_words": df["num_words"],
            "num_characters": df["num_characters"],
        }
    )

    return speeches_df
