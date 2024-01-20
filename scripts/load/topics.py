import pandas as pd
import transform.topics as topics


def dataframe(date_yyyymmdd, topics_list):
    titles = [section["title"] for section in topics_list]
    subtitles = [section["subTitle"] for section in topics_list]
    section_types = [section["sectionType"] for section in topics_list]
    question_counts = [section["questionCount"] for section in topics_list]

    orders = list(range(1, len(topics_list) + 1))

    topic_cids = [topics.topic_cid(date_yyyymmdd, order) for order in orders]

    topics_df = pd.DataFrame(
        {
            "Date": [date_yyyymmdd] * len(topics_list),
            "Topic_CID": topic_cids,
            "Order": orders,
            "Title": titles,
            "Subtitle": subtitles,
            "Section_Type": section_types,
            "Question_Count": question_counts,
        }
    )

    return topics_df
