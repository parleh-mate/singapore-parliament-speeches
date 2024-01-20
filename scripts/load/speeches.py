import pandas as pd
import transform.topics as topics
import transform.speeches as speeches

def dataframe(date_yyyymmdd, topics_list):

    speeches_df = None

    orders = list(range(1, len(topics_list) + 1))
    topic_cids = [topics.topic_cid(date_yyyymmdd, order) for order in orders]

    for index, topic in enumerate(topics_list):
        topic_cid = topic_cids[index]
        temp_df = speeches.topic_dataframe(topic["content"], 
                                           topic_cid, 
                                           index)

        if speeches_df is None:
            speeches_df = temp_df
        else:
            speeches_df = pd.concat([speeches_df,
                                    temp_df],
                                    ignore_index=True)
    
    speech_orders = list(range(1, len(speeches_df) + 1))
    speeches_df['Speech_Order'] = speech_orders
    speeches_df['Speech_CID'] = speeches_df.apply(speeches.speech_cid, axis = 1)

    return speeches_df