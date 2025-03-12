import pandas as pd
import transform.topics as topics


def dataframe(date_yyyymmdd, topics_list):
    orders = list(range(1, len(topics_list) + 1))
    topic_cids = [topics.topic_cid(date_yyyymmdd, order) for order in orders]

    topics_df = pd.DataFrame(
        {
            "topic_id": topic_cids,
            "date": [date_yyyymmdd] * len(topics_list),
            "topic_order": orders,
            "title": [section["title"] for section in topics_list],
            "section_type": [section["sectionType"] for section in topics_list],
        }
    )

    return topics_df
